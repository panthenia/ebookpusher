import requests,pickle

f = open('d:\\a.data','rb')
r = pickle.load(f)
f.close()
print(r.)
cookie = requests.utils.dict_from_cookiejar(r.cookies)
print(cookie)