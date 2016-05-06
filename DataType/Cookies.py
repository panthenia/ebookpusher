import time


class Cookies(object):

    def __init__(self):
        self.cookieValues = {}
        self.minExpires = float('inf')

    def isValid(self):
        if self.minExpires == float('inf'):
            return False

        cstamp = time.time()
        if abs(self.minExpires - cstamp) >= 600:
            return True
        else:
            return False

    def addCookie(self, name, value, expires):
        self.cookieValues[name] = value
        try:
            ex = float(expires)
        except Exception:
            ex = float('inf')
        if ex < self.minExpires:
            self.minExpires = ex

    def toDict(self):
        return self.cookieValues

