# from Utils.BookDownloader import BookDownloader
# from DataType.BookTypes import BookSummary
# import json
# down = BookDownloader()
# sumary = BookSummary(name='', id='39409')
# detail = down.getBookDetail(summary=sumary)
# print(json.dumps(detail, default=lambda o:o.__dict__, ensure_ascii=False))
from bs4 import BeautifulSoup

soup = BeautifulSoup('''<div class="fl metainfo">
                <span class="gray">副标题: </span>透过文本看中国侠史<br>
                <span class="gray">作者: </span>马步升<br>
        <span class="gray">添加于: </span><abbr class="timeago" title="2016-05-16 14:02:45">2016-05-16 14:02:45</abbr><br>

                <span class="gray">参考网站: </span><a href="https://book.douban.com/subject/4715161/ " target="_blank">豆瓣</a><br>
                <!-- <span class="gray">下载: </span>3次<br>

        <span class="gray">推送: </span>0次<br> -->
        <!--
        <span class="gray">查看: </span>0次<br>
        -->
                        <span class="gray">ISBN: </span>9787805878812<br>
                                          </div>''', 'html5lib')
# print(soup.prettify())
spans = soup.find_all('span', attrs={'class': 'gray'})
metas = {}
for x in spans:
    if x.string:
        us = str(x.string.encode('utf-8'), 'utf-8')
        if not '添加于' in us:
            if '参考网站' in us:
                metas[x.next_sibling.string] = x.next_sibling['href']
            else:
                metas[us[0:len(us)-2]] = x.next_sibling
print(metas)