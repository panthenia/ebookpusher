from bs4 import BeautifulSoup
import os
soup = BeautifulSoup('''<div class="fl metainfo">
                <span class="gray">作者: </span> 史蒂芬・霍金<br>
        <span class="gray">添加于: </span><abbr class="timeago" title="2012-03-31 21:19:31">2012-03-31 21:19:31</abbr><br>

                <span class="gray">参考网站: </span><a href="http://book.douban.com/subject_search?search_text=9787535715791" target="_blank">豆瓣</a><br>
                <!-- <span class="gray">下载: </span>309次<br>

        <span class="gray">推送: </span>66次<br> -->
        <!--
        <span class="gray">查看: </span>0次<br>
        -->
                        <span class="gray">ISBN: </span>9787535715791<br>
                      </div>''', 'html5lib')


os.path.isdir