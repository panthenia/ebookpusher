import requests
from Utils import LoginHelper
from Utils.DataBaseHelper import DbHelper
from bs4 import BeautifulSoup
from DataType.BookTypes import *
import re

seach_url = 'https://www.mlook.mobi/search'


def seachBook(bookname):
    dbhelper = DbHelper()
    cookies = dbhelper.getCookies()

    # 如果数据库中的cookies已经过期则重新获取
    if not cookies.isValid():
        user = dbhelper.getUser()
        lghelper = LoginHelper.LoginHelper(user[0], user[1])
        cookies = lghelper.login()

    r = requests.get(url=seach_url, params={'q': bookname},
                     headers=LoginHelper.login_headers, cookies=cookies.toDict())
    dbhelper.close()
    return parseSeachResult(r.text)


def parseNameAndUrl(div):
    h3 = div.find('h3')
    namept = ''
    for x in h3.a.stripped_strings:
        namept += x
    sp = h3.find('span', attrs={'class': 'fs12'})
    if sp is not None:
        des = next(sp.stripped_strings)
        sigstr = significantStr(des)
        if not sigstr in namept:
            namept += des
    url = 'https://www.mlook.mobi' + h3.a['href']
    return namept, url


def parseSeachResult(html):
    result = []
    soup = BeautifulSoup(html, 'html5lib')
    bdivs = soup.find_all('div', attrs={'class': 'book clearfix'})
    for div in bdivs:
        img = div.find('img', src=re.compile('^https://www.mlook.mobi/img/'))['src']
        name, url = parseNameAndUrl(div)
        ori_arthur = next(div.find('div', attrs={'class': 'fl meta'}) \
                          .find('p', attrs={'class': 'gray counters'}).stripped_strings)
        arthur = ori_arthur[0: ori_arthur.find('上传于')]
        abk = BookSeachResult(name=name, url=url, img=img, arthur=arthur)
        result.append(abk)
    return result

def getBookDetail(link):
    dbhelper = DbHelper()
    cookies = dbhelper.getCookies()

    # 如果数据库中的cookies已经过期则重新获取
    if not cookies.isValid():
        user = dbhelper.getUser()
        lghelper = LoginHelper.LoginHelper(user[0], user[1])
        cookies = lghelper.login()

    r = requests.get(url=link,
                     headers=LoginHelper.login_headers, cookies=cookies.toDict())
    dbhelper.close()
    return parseBookDetail(r.text)

def parseBookDetail(html):
    pass

# 判断一个字符是否汉字字母或数字
def isSignificantWord(w):
    if '\u4E00'<=w<='\u9FA5' or '\u0030'<=w<='\u0039' or '\u0061'<=w<='\u007a' or '\u0041'<=w<='\u005a':
        return True
    else:
        return False

def significantStr(s):
    ns = ''
    for w in s:
        if isSignificantWord(w):
            ns+=w
    return ns
books = seachBook('时间简史')
for book in books:
    print(book)
