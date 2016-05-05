import requests
from Utils import LoginHelper,DataBaseHelper

down_header = LoginHelper.login_headers.copy()
down_header['Host'] = 'down.mlook.mobi'


class BookDownloader(object):
    def __init__(self, booklink):
        self.booklink = booklink

    def downloadBook(self):
        dbhelper = DataBaseHelper.DbHelper()
        cookies = dbhelper.getCookies()
        user = dbhelper.getUser()
        if not cookies.isValid():
            loghelper = LoginHelper.LoginHelper(user[0],user[1])
            cookies = loghelper.login()
            r = requests.get(url=self.booklink, headers=down_header, cookies=cookies.toDict())
            # requests 库自动处理了重定向,新的url在r.url字段中
            split_url = r.url.split('/')
            print(split_url, len(split_url))

            down_url = 'http://down.mlook.mobi/'
            for i in range(3, len(split_url)):
                down_url += '/' + split_url[i]

            r = requests.get(url=down_url, headers=down_header, cookies=cookies.toDict())

            f = open(self.parseBookeName(down_url), 'wb')
            f.write(r.content)
            f.close()

    def parseBookeName(self, url):
        namepart = url.split('/')[5]
        return namepart.split('?')[0]




