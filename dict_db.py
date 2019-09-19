"""
数据库处理操作
"""
import pymysql
import hashlib

def encryption(passwd):
    salt = "^$5eD4#a"
    hash = hashlib.md5(salt.encode())
    hash.update(passwd.encode())
    return hash.hexdigest()

class User:
    def __init__(self, host = 'localhost',
                 port = 3306,
                 user='root',
                 passwd='123456',
                 database='dict',
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标对象
    def create_cursor(self):
        self.cur = self.db.cursor()

    def register(self, name, passwd):
        sql = "select * from user where name=%s"
        self.cur.execute(sql, [name])
        r = self.cur.fetchone()
        # 查找到说明用户存在
        if r:
            return False

        # 插入用户名密码
        sql = "insert into user (name,passwd) \
            values (%s,%s)"
        passwd = encryption(passwd)  # 加密处理
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        sql = "select * from user \
            where name=%s and passwd=%s"
        passwd = encryption(passwd)
        self.cur.execute(sql, [name, passwd])
        r = self.cur.fetchone()
        # 查找到则登录成功
        if r:
            return True
        else:
            return False

    def query(self, word):
        sql = "select mean from my_dictionary \
         where word = %s"
        self.cur.execute(sql, [word])
        mean = self.cur.fetchone()
        # 是否查找
        if mean:
            return mean[0]

    def do_record(self,name,word):
        sql = "insert into hist(name, word)\
         values(%s, %s)"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def do_get_record(self, name):
        sql = "select name,word,time from hist where\
         name = %s order by time desc limit 10;"
        self.cur.execute(sql, [name])
        # 返回历史记录
        return self.cur.fetchall()

if __name__ == '__main__':
    user = User()

    # if user.register('Abby','123'):
    #     print("注册成功")

    if user.login('Abby', '123'):
        print("登录成功")