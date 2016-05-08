from Utils import DataBaseHelper
import urllib
import requests
from bs4 import BeautifulSoup
from DataType.BookTypes import *
from DataType.Cookies import Cookies
import re

login_url = 'https://www.mlook.mobi/member/login'
login_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                 'Accept-Encoding': 'gzip, deflate, sdch',
                 'Accept-Language': 'zh-CN,zh;q=0.8',
                 'Cache-Control': 'max-age=0',
                 'Connection': 'keep-alive',
                 'Host': 'www.mlook.mobi',
                 'Upgrade-Insecure-Requests': '1',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
login_form = {'f': 'https://www.mlook.mobi/',
              'person[remember_me]': '1',
              'commit': '登录'}
seach_url = 'https://www.mlook.mobi/search'
down_header = login_headers.copy()
down_header['Host'] = 'down.mlook.mobi'


class BookDownloader(object):
    def __init__(self):
        self.dbhelper = DataBaseHelper.DbHelper()
        self.cookies = self.dbhelper.getCookies()
        self.session = requests.session()

    # 如果数据库中的cookies已经过期则重新获取
    def updateCookies(self):

        if not self.cookies.isValid():
            user = self.dbhelper.getUser()
            self.cookies = self.login(user)

    def downloadBook(self, booklink, folder = None):
        """
        用于下载一本书
        :param booklink: 书籍的地址
        :param folder: 下载的目的路径
        :return: None
        """
        self.updateCookies()

        # requests 库自动处理了重定向,新的url在r.url字段中
        r = self.session.get(url=booklink,
                         headers=down_header,
                         cookies=self.cookies.toDict())
        split_url = r.url.split('/')
        print(split_url, len(split_url))

        down_url = 'http://down.mlook.mobi/'
        for i in range(3, len(split_url)):
            down_url += '/' + split_url[i]

        r = self.session.get(url=down_url,
                         headers=down_header,
                         cookies=self.cookies.toDict())

        bookName = self.parseBookeName(down_url)
        bookName = urllib.parse.unquote(bookName)
        f = open(bookName, 'wb')
        f.write(r.content)
        f.close()

    def parseBookeName(self, url):
        """
        从书籍地址中解析书籍名字

        :param url: 书籍地址
        :return: 书字
        """
        namepart = url.split('/')[-1]
        return namepart.split('?')[0]

    def login(self, user):
        """
        Cookie过期后登录重新获取Cookie,得到新的cookie后会存入数据库中
        :param user: 账户信息
        :return: 返回新的cookie
        """

        # 获取登录页面的formhash值
        r = self.seesion.get(url=login_url, headers=login_headers)
        soup = BeautifulSoup(r.text, "html5lib")
        formhash = soup.find(attrs={'name': 'formhash'})['value']
        login_form['formhash'] = formhash

        # 登录
        login_form['person[login]'] = user[0]
        login_form['person[password]'] = user[1]
        r = self.seesion.post(url=login_url, headers=login_headers, data=login_form)
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            return None

        cookies = Cookies()
        for cookie in self.seesion.cookies:
            cookies.addCookie(cookie.name, cookie.value, cookie.expires)
        self.dbhelper.saveCookies(cookies)
        return cookies

    def seachBook(self, bookname):
        """
        搜索书籍
        :param bookname:书名
        :return: 见parseSeachResult
        """
        self.updateCookies()
        r = self.session.get(url=seach_url, params={'q': bookname},
                         headers=login_headers, cookies=self.cookies.toDict())
        return self.parseSeachResult(r.text)

    def parseNameAndUrl(self, div):
        h3 = div.find('h3')
        namept = ''
        for x in h3.a.stripped_strings:
            namept += x
        sp = h3.find('span', attrs={'class': 'fs12'})
        if sp is not None:
            des = next(sp.stripped_strings)
            sigstr = self.significantStr(des)
            if not sigstr in namept:
                namept += des
        url = 'https://www.mlook.mobi' + h3.a['href']
        return namept, url

    def parseSeachResult(self, html):
        result = []
        soup = BeautifulSoup(html, 'html5lib')
        bdivs = soup.find_all('div', attrs={'class': 'book clearfix'})
        for div in bdivs:
            img = div.find('img', src=re.compile('^https://www.mlook.mobi/img/'))['src']
            name, url = self.parseNameAndUrl(div)
            ori_arthur = next(div.find('div', attrs={'class': 'fl meta'}) \
                              .find('p', attrs={'class': 'gray counters'}).stripped_strings)
            arthur = ori_arthur[0: ori_arthur.find('上传于')]
            abk = BookSeachResult(name=name, url=url, img=img, arthur=arthur)
            result.append(abk)
        return result

    def getBookDetail(self, link):
        self.updateCookies()
        r = requests.get(url=link,
                         headers=login_headers, cookies=self.cookies.toDict())
        return self.parseBookDetail(r.text)

    def parseBookDetail(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        ts = soup.find('div', attrs={'class': 'fl metainfo'}).stripped_strings

        meta = [x for x in ts]
        di = meta.index('添加于:')
        del meta[di]
        del meta[di + 1]

        ts = soup.find('div', attrs={'class': 'intro'}).stripped_strings
        des = [x for x in ts]

        downlink = []
        booksdivs = soup.find('div', attrs={'class': 'ebooks'}).find_all('div', attrs={'class': 'ebook clearfix'})
        for book in booksdivs:
            a = book.find('a', attrs={'class': 'download'})
            link = 'https://www.mlook.mobi' + a['href']
            type = a['original-title']
            downlink.append((link, type,))

        detail = BookDetail(meta, des, downlink)
        return detail

    # 判断一个字符是否汉字字母或数字
    def isSignificantWord(self, w):
        if '\u4E00' <= w <= '\u9FA5' or '\u0030' <= w <= '\u0039' or '\u0061' <= w <= '\u007a' or '\u0041' <= w <= '\u005a':
            return True
        else:
            return False

    def significantStr(self, s):
        ns = ''
        for w in s:
            if self.isSignificantWord(w):
                ns += w
        return ns

    def close(self):
        self.session.close()
        self.dbhelper.close()




