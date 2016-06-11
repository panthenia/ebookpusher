# from Utils.BookDownloader import BookDownloader
# from DataType.BookTypes import BookSummary
# import json
# down = BookDownloader()
# sumary = BookSummary(name='', id='39409')
# detail = down.getBookDetail(summary=sumary)
# print(json.dumps(detail, default=lambda o:o.__dict__, ensure_ascii=False))
from bs4 import BeautifulSoup
from bs4.element import NavigableString
t = tuple()
print(len(t))
tt =(1,2,3,4,)
print(tt[0:2],type(tt[0:2]))


# soup = BeautifulSoup('''<div class="fl metainfo">
#                 <span class="gray">副标题: </span>透过文本看中国侠史<br>
#                 <span class="gray">作者: </span>马步升<br>
#         <span class="gray">添加于: </span><abbr class="timeago" title="2016-05-16 14:02:45">2016-05-16 14:02:45</abbr><br>
#
#                 <span class="gray">参考网站: </span><a href="https://book.douban.com/subject/4715161/ " target="_blank">豆瓣</a><br>
#                 <!-- <span class="gray">下载: </span>3次<br>
#
#         <span class="gray">推送: </span>0次<br> -->
#         <!--
#         <span class="gray">查看: </span>0次<br>
#         -->
#                         <span class="gray">ISBN: </span><br>
#                                           </div>''', 'html5lib')
#
# mdiv = soup.find('div', attrs={'class': 'fl metainfo'})
# spans = mdiv.find_all('span', attrs={'class': 'gray'})
# for x in spans:
#     if x.string:
#         us = str(x.string.encode('utf-8'), 'utf-8')
#         print(us)
#         print(x.next_sibling, type(x.next_sibling))
#         if isinstance(x.next_sibling,NavigableString):
#             print(str(x.next_sibling))
#         if '参考网站' in us:
#             print(x.next_sibling['href'], type(x.next_sibling['href']))
# # print(soup.prettify())
# spans = soup.find_all('span', attrs={'class': 'gray'})
# metas = {}
# for x in spans:
#     if x.string:
#         us = str(x.string.encode('utf-8'), 'utf-8')
#         if not '添加于' in us:
#             if '参考网站' in us:
#                 metas[x.next_sibling.string] = x.next_sibling['href']
#             else:
#                 metas[us[0:len(us)-2]] = x.next_sibling
# print(metas)
# import urllib.parse
# a = ['d0c9GChOYGWub4ydnQw069To16Cfpdcj40zn5L4nuOkvTQ',
#      'aaacWAd8e2nmxTflM7YtxCoCBvkZhNagUR9RoJWt1W8qGg',
# '28504MYieyZtmctKbvoOFeuDmgX3yHeg2qhGHis5zeVr%2FQ',
# 'e1edtRynHqHaNUSDdP6h5UKGJJWxR6eX3aR%2FLUJAPNTZ4Q',
# 'ece8n6easI%2FxzngysfcAkQIWw%2FBzJK7sHTAJch0PgMN%2B%2Fw',
# '809faAfHH6UjYw8gxvo0zocbgRFFVW%2BGlub8vErUaUSX5A',
# '1fc087sEnvOXsbMHvfZaO7K3c3iLrEJOqxdQEEVt0K8krw',
# 'fbe1LFMPwsq8ap67fHf7Wq5apym6wv15W3tiUJWlLygA4Q']
#
# a = (1,2,)
# b = (3,4)
# print(a+b)