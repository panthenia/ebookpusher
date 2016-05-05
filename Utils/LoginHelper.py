import requests
from bs4 import BeautifulSoup
from DataType.Cookies import Cookies
from Utils.DataBaseHelper import DbHelper

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


class LoginHelper(object):

    def __init__(self, act, psw):
        self.account = act
        self.password = psw
        self.seesion = requests.session()

    def login(self):

        # 获取登录页面的formhash值
        r = self.seesion.get(url=login_url, headers=login_headers)
        soup = BeautifulSoup(r.text, "html5lib")
        formhash = soup.find(attrs={'name': 'formhash'})['value']
        login_form['formhash'] = formhash

        # 登录
        login_form['person[login]'] = self.account
        login_form['person[password]'] = self.password
        r = self.seesion.post(url=login_url, headers=login_headers, data=login_form)
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            return None

        cookies = Cookies()
        for cookie in self.seesion.cookies:
            cookies.addCookie(cookie.name, cookie.value, cookie.expires)
        dbhelper = DbHelper()
        dbhelper.saveCookies(cookies)
        dbhelper.close()
        return cookies






