import sqlite3
from DataType.Cookies import Cookies
import os
CREATE_COOKIES_TABLE = 'CREATE TABLE IF NOT EXISTS cookies (cname TEXT,cvalue TEXT,cexpires REAL)'
CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS user (account TEXT,password TEXT)'
CLEAR_COOKIES_TABLE = 'DELETE FROM cookies'

DBFILE_NAME = os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'ebookpush.db')


class DbHelper(object):
    def __init__(self):
        self.con = sqlite3.connect(DBFILE_NAME)
        print(DBFILE_NAME)
        cursor = self.con.cursor()
        cursor.execute(CREATE_COOKIES_TABLE)
        cursor.execute(CREATE_USER_TABLE)
        self.con.commit()
        cursor.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.con.close()

    def saveCookies(self, cookies: Cookies):
        cursor = self.con.cursor()
        cursor.execute(CLEAR_COOKIES_TABLE)
        cdicts = cookies.toDict()
        for x in cdicts.keys():
            self.con.execute('insert into cookies VALUES (?,?,?)', (x, cdicts[x], cookies.minExpires,))
        cursor.close()
        self.con.commit()

    def getCookies(self):
        cursor = self.con.cursor()
        cursor.execute('select * from cookies')
        cks = cursor.fetchall()
        cookies = Cookies()
        tm = .0
        for ck in cks:
            cookies.addCookie(ck[0], ck[1])
            tm = float(ck[2])
        cookies.minExpires = tm
        cursor.close()
        self.con.commit()
        return cookies

    def saveUser(self, act, psw):
        cursor = self.con.cursor()
        cursor.execute('insert into user VALUES (?,?)', (act, psw,))
        self.con.commit()
        cursor.close()
        pass

    def getUser(self):
        cursor = self.con.cursor()
        cursor.execute('select * from user')
        result = cursor.fetchall()
        cursor.close()
        self.con.commit()
        return result[0]

    def getPushEmailAccount(self):
        cursor = self.con.cursor()
        cursor.execute('select * from email')
        result = cursor.fetchall()
        cursor.close()
        self.con.commit()
        return result[0]