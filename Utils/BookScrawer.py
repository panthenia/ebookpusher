import requests, multiprocessing
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import mysql.connector


class BookDetail(object):
    def __init__(self, mt: dict, des: [str], down: [dict]):
        self.meta = mt
        """:type : dict"""
        self.isbn = mt.get('isbn', ' ')
        self.name = mt.get('name', ' ')
        self.douban_rate = mt.get('douban_rate', ' ')
        self.douban_link = mt.get('douban_link', ' ')
        self.arthur = mt.get('arthur', ' ')

        self.des = des
        """:type : [str]"""

        self.downInfo = down
        """:type : [dict]
            dict_example = {
                "link":link_url,
                "type":book_type
            }

        """

    def __str__(self, *args, **kwargs):
        super().__str__(*args, **kwargs)
        return str(self.meta)

    def to_tuple(self):
        desc = ''
        for x in self.des:
            desc += x + '\n'
        return self.isbn, self.arthur, self.name, self.douban_rate, self.douban_link, desc


def parseBookDetail(html: str) -> BookDetail:
    """
    用于解析获取到的书籍信息的HTML文件
    :return: 返回一个BookDetail对象
    """
    soup = BeautifulSoup(html, 'html5lib')
    metas = {}
    mdiv = soup.find('div', attrs={'class': 'fl metainfo'})
    if mdiv:
        metas['name'] = str.strip(mdiv.parent.parent.find('h1').string)
        spans = mdiv.find_all('span', attrs={'class': 'gray'})
        for x in spans:
            if x.string:
                us = str(x.string.encode('utf-8'), 'utf-8')
                if not '添加于' in us:
                    if '参考网站' in us:
                        metas['douban_link'] = '' if '暂无' in us else x.next_sibling['href']
                    elif 'ISBN' in us:
                        metas['isbn'] = str(x.next_sibling) if isinstance(x.next_sibling, NavigableString) else ''

                    elif '作者' in us:
                        metas['arthur'] = str(x.next_sibling) if isinstance(x.next_sibling, NavigableString) else ''
                    elif '豆瓣评分' in us:
                        metas['douban_rate'] = str(x.next_sibling) if isinstance(x.next_sibling, NavigableString) else ''

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

        detail = BookDetail(metas, des, downlink)
        return detail


def get_page(q: multiprocessing.Queue, book_id):

    url = 'https://www.mlook.mobi/book/info/' + str(book_id)

    page_html = requests.get(url=url).text
    detail = parseBookDetail(page_html)
    if detail is not None:
        # print(detail)
        # print(detail.to_tuple())
        q.put(detail.to_tuple()+(book_id,))


def database_writer(q: multiprocessing.Queue, max):
    con = mysql.connector.connect(host='localhost',
                          user='root',
                          password='12345678',
                          database='book')
    print('start db_write_process')
    count = 0
    cursor = con.cursor()
    flag = True
    while flag:
        try:
            # Create a new record
            sql = "INSERT INTO book_info VALUES (%s,%s,%s,%s,%s,%s,%s)"
            data = q.get(block=True)
            if count == max:
                flag = False
            else:
                cursor.execute(sql, data[0:7])
                con.commit()
                count += 1
                print(data[6])


        except Exception as e:
            print(e.args)
    print('writer process finished')
    cursor.close()
    con.close()


if __name__ == '__main__':
    min_val = 22935
    max_val = 39886
    pool = multiprocessing.Pool(processes=4)
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    wt_process = multiprocessing.Process(target=database_writer, args=(queue, max_val))
    wt_process.start()
    for x in range(min_val, max_val+1):
        pool.apply_async(func=get_page, args=(queue, x))
    pool.close()
    pool.join()
    wt_process.join()
    print('finished')
