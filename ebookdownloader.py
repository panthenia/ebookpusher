import requests
import pickle

url = 'https://www.mlook.mobi/member/login'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'www.mlook.mobi',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}
form = {'f': 'https://www.mlook.mobi/',
        'formhash': 'f14239cddda5be4c',
        'person[login]': '2309623743@qq.com',
        'person[password]': 'lipan1234',
        'person[remember_me]': '0',
        'person[remember_me]': '1',
        'commit': '登录'}

param = {'q': '活着'}

s = requests.session()
r = s.post(url=url, headers=headers, data=form)
cks = requests.utils.dict_from_cookiejar(s.cookies)
r = s.get(url='https://www.mlook.mobi/search', headers=headers, params=param, cookies=cks)
print(r.text)
# f = open('d:\\a.data', 'wb')
# pickle.dump(r, f)
