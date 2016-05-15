from Utils.DataBaseHelper import DbHelper
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

download_chunk_size = 10*1024

class BookDownloader(object):
    def __init__(self):

        with DbHelper() as dbhelper:
            self.cookies = dbhelper.getCookies()
            """:type : Cookies"""

        self.session = requests.session()
        """:type : request.Session"""

    # 如果数据库中的cookies已经过期则重新获取
    def checkCookies(self):

        if not self.cookies.isValid():
            self.updateCookies()

    def updateCookies(self):
        with DbHelper() as dbhelper:
            user = dbhelper.getUser()
            if user is not None:
                self.cookies = self.login(user)

    def downloadBook(self, booklink, folder=None) -> None:
        """
        用于下载一本书
        :param booklink: 书籍的地址
        :param folder: 下载的目的路径
        :return: None
        """
        self.checkCookies()

        # requests 库自动处理了重定向,新的url在r.url字段中
        r = self.session.get(url=booklink,
                             headers=down_header,
                             cookies=self.cookies.toDict())
        split_url = r.url.split('/')
        print(split_url, len(split_url))

        down_url = 'http://down.mlook.mobi/'
        for i in range(3, len(split_url)):
            down_url += '/' + split_url[i]

        try:
            r = self.session.get(url=down_url,
                                stream=True,
                                headers=down_header,
                                cookies=self.cookies.toDict())
        except Exception as e:
            print(e)

        if 'Transfer-Encoding' in r.headers:
            print('file transfer type is:%s'%r.headers['Transfer-Encoding'])
        elif 'Content-Length' in r.headers:
            print('file size is : %s' % r.headers['Content-Length'])

        bookName = self.parseBookeName(down_url)
        bookName = urllib.parse.unquote(bookName)
        with open(bookName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=download_chunk_size):
                if chunk:
                    f.write(chunk)
                    print('%s bytes received' % len(chunk))

    def parseBookeName(self, url) -> str:
        """
        从书籍地址中解析书籍名字
        :param url: 书籍地址
        :return: 书名
        """
        namepart = url.split('/')[-1]
        return namepart.split('?')[0]

    def login(self, user) -> Cookies:
        """
        Cookie过期后登录重新获取Cookie,得到新的cookie后会存入数据库中
        :param user: 账户信息
        :return: 返回新的cookie
        """

        # 获取登录页面的formhash值
        r = self.session.get(url=login_url, headers=login_headers)
        soup = BeautifulSoup(r.text, "html5lib")
        formhash = soup.find(attrs={'name': 'formhash'})['value']
        login_form['formhash'] = formhash

        # 登录
        login_form['person[login]'] = user[0]
        login_form['person[password]'] = user[1]
        r = self.session.post(url=login_url, headers=login_headers, data=login_form)
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            return None

        cookies = Cookies()
        for cookie in self.session.cookies:
            cookies.addCookie(cookie.name, cookie.value)
        with DbHelper() as dbhelper:
            dbhelper.saveCookies(cookies)
        return cookies

    def seachBook(self, bookname) -> [BookSummary]:
        """
        搜索书籍
        :param bookname:书名
        :return: 见parseSeachResult
        """
        self.checkCookies()

        r = self.session.get(url=seach_url, params={'q': bookname},
                             headers=login_headers, cookies=self.cookies.toDict())
        return self.parseSeachResult(r.text)

    def parseNameAndUrl(self, div) -> (str, str,):
        """
        用于解析出搜索结果中书籍的名字和URL
        :param div:搜索结果中一本书的信息html文档
        :return:返回该书的名字和地址
        """
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

    def parseSeachResult(self, html: str) -> [BookSummary]:
        """
        用于解析搜索结果的HTML
        :param html: 搜索得到的HTML
        :return: 返回格式为一个包含若干BookSeachResult的列表: [BookSeachResult]
        """
        result = []
        soup = BeautifulSoup(html, 'html5lib')
        bdivs = soup.find_all('div', attrs={'class': 'book clearfix'})
        for div in bdivs:

            # img地址处理:把后缀的——66——88去掉得到大图
            img = div.find('img', src=re.compile('^https://www.mlook.mobi/img/'))['src']
            img = self.handle_image_url(img)

            name, url = self.parseNameAndUrl(div)
            ori_arthur = next(div.find('div', attrs={'class': 'fl meta'}) \
                              .find('p', attrs={'class': 'gray counters'}).stripped_strings)
            arthur = ori_arthur[0: ori_arthur.find('上传于')]
            abk = BookSummary(name=name, id=url.split('/')[-1], img=img, arthur=arthur)
            result.append(abk)
        return result

    def handle_image_url(self, url):
        rurl = url[::-1]
        spl = rurl.split('_', maxsplit=2)
        qt = spl[0].split('.')[0] + '.' + spl[2]
        result = qt[::-1]
        return result

    def getBookDetail(self, summary: BookSummary) -> BookDetail:
        """
        用于访问书籍地址,获取书籍的具体信息
        :param summary: 输入为书籍的摘要信息
        :return: 返回一个BookDetail对象,参见parseBookDetail
        """
        self.checkCookies()
        url = 'https://www.mlook.mobi/book/info/'+summary.bookid
        r = requests.get(url=url,
                         headers=login_headers, cookies=self.cookies.toDict())
        return self.parseBookDetail(r.text)

    def parseBookDetail(self, html: str) -> BookDetail:
        """
        用于解析获取到的书籍信息的HTML文件
        :param html: 书籍的HTML
        :return: 返回一个BookDetail对象
        """
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
            ltdict = {}
            ltdict['link'] = 'https://www.mlook.mobi' + a['href']
            ltdict['type'] = a['original-title']
            downlink.append(ltdict)

        detail = BookDetail(meta, des, downlink)
        return detail

    def isSignificantWord(self, w) -> bool:
        """
        判断一个字符是否汉字字母或数字
        :param w: 需要判断的字符
        :return:返回判断结果
        """
        if '\u4E00' <= w <= '\u9FA5' or '\u0030' <= w <= '\u0039' or '\u0061' <= w <= '\u007a' or '\u0041' <= w <= '\u005a':
            return True
        else:
            return False

    def significantStr(self, s) -> str:
        """
        提取一个字符串中的汉字字母或数字,去除其他字符
        :param s: 需要提取的原始字符串
        :return: 返回提取后的字符串
        """
        ns = ''
        for w in s:
            if self.isSignificantWord(w):
                ns += w
        return ns

    def close(self) -> None:
        self.session.close()
        self.dbhelper.close()
