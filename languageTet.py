from bs4 import BeautifulSoup
import re
soup = BeautifulSoup('''<h3>
            <a href="/book/info/1442">嘟嘟<span class="red">时间简史</span>hah</a>
                        <span class="fs12"> : 插图本</span>
                                    <a class="comments" href="/book/info/1442#comments2">2</a>
                      </h3>''', 'html5lib')
a = ':作者：史蒂芬.霍金 上传于'

for x in a:
    if x >='\u4E00' and x <= '\u9FA5':
        print(x+'yes\n')
    else:
        print(x+'no\n')

