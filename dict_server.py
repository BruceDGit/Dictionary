"""

"""
from socket import *
from multiprocessing import Process
import sys, signal
from time import sleep

import dict_db

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
db = dict_db.User(database='dict')  # 数据库对象


def do_register(connfd, data):
    # 注册
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name, passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'Fail')


def do_login(connfd, data):
    # 登录
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'Fail')


def do_search(connfd, data):
    # 查单词
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    mean = db.query(word)
    if mean:
        connfd.send(mean.encode())
        db.do_record(name, word)
    else:
        connfd.send(b'error')


def get_history(connfd, data):
    # 查记录
    tmp = data.split(' ')
    name = tmp[1]
    hist = db.do_get_record(name)
    if not hist:
        connfd.send(b'##')
        connfd.send(hist.encode())
    else:
        for item in hist:
            msg = "%s %-16s %s"%item
            connfd.send(msg.encode())
            sleep(0.05)
    connfd.send(b'##')


def request(connfd):
    # 处理客户端各种请求
    db.create_cursor()  # 每个子进程有自己的游标
    while True:
        data = connfd.recv(1024).decode() # 接收请求
        if not data or data[0] == 'E':
            sys.exit("客户端退出")  # 退出对应的子进程
        elif data[0] == 'R':
            do_register(connfd, data)
        elif data[0] == 'L':
            do_login(connfd, data)
        elif data[0] == 'Q':
            do_search(connfd, data)
        elif data[0] == 'H':
            get_history(connfd, data)

#搭建网络
def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端链接
    print("Listen the prot 8888")
    while True:
        try:
            c, addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sys.exit("服务退出")
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        p = Process(target=request, args=(c,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()