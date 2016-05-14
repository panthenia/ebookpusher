import json


class BookSummary(object):
    def __init__(self, name:str, id:str, img:str=None, arthur:str=None):
        self.name = name
        """:type : str"""

        self.bookid = id
        """:type : str"""

        self.img = img
        """:type : str"""

        self.arthur = arthur
        """:type : str"""
    def __str__(self, *args, **kwargs):
        super().__str__(*args, **kwargs)
        return 'BookInfo:\nname:{0},url:{1},img:{2},arthur:{3}'\
            .format(self.name, self.url, self.img, self.arthur)

    def to_json(self):
        return json.dumps(self,default=lambda o:o.__dict__)


class BookDetail(object):
    def __init__(self, mt: [str], des: [str], down: [dict]):
        self.meta = mt
        """:type : [str]"""

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
        return str(self.downInfo)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

