import time


class Cookies(object):

    def __init__(self):
        self.cookieValues = {}
        self.minExpires = time.time()

    def isValid(self):

        cstamp = time.time()
        if abs(self.minExpires - cstamp) > 86400:
            return False
        else:
            return True

    def addCookie(self, name, value):
        self.cookieValues[name] = value

    def toDict(self):
        return self.cookieValues

