import sqlite3
from DataType.Cookies import Cookies
CREATE_COOKIES_TABLE = 'CREATE TABLE IF NOT EXISTS cookies (cname TEXT,cvalue TEXT,cexpires REAL)'
CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS user (account TEXT,password TEXT)'
CLEAR_COOKIES_TABLE = 'DELETE * FROM TABLE cookies'

DBFILE_NAME = 'ebookpush.db'


class DbHelper(object):
    def __init__(self):
        self.con = sqlite3.connect(DBFILE_NAME)
        self.con.execute(CREATE_COOKIES_TABLE)
        self.con.execute(CREATE_USER_TABLE)

    def close(self):
        self.con.commit()
        self.con.close()

    def saveCookies(self, cookies: Cookies):
        self.con.execute(CLEAR_COOKIES_TABLE)
        cdicts = cookies.toDict()
        for x in cdicts.keys():
            self.con.execute('insert into cookies VALUES (?,?,?)', (x, cdicts[x], cookies.minExpires,))
        self.con.commit()

    def getCookies(self):
        cursor = self.con.cursor()
        cursor.execute('select * from cookies')
        cks = cursor.fetchall()
        cookies = Cookies()
        for ck in cks:
            cookies.addCookie(ck[0], ck[1], ck[2])
        cursor.close()
        return cookies

    def saveUser(self):
        pass

    def getUser(self):
        cursor = self.con.cursor()
        cursor.execute('select * from user')
        user = cursor.fetchall()
        cursor.close()
        return user[0]
