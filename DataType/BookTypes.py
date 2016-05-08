class BookSeachResult(object):
    def __init__(self, name, url, img=None, arthur=None):
        self.name = name
        self.url = url
        self.img = img
        self.arthur = arthur

    def __str__(self, *args, **kwargs):
        super().__str__(*args, **kwargs)

        return 'BookInfo:\nname:{0},url:{1},img:{2},arthur:{3}'\
            .format(self.name, self.url, self.img, self.arthur)


class BookDetail(object):
    def __init__(self, mt, des, down):
        self.meta = mt
        self.des = des
        self.downInfo = down

    def __str__(self, *args, **kwargs):
        super().__str__(*args, **kwargs)

        return str(self.downInfo)

