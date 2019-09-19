"""
dict 客户端

功能：发起请求，接收结果
"""
from socket import *
import sys
import getpass


# 服务器地址
ADDR = ('127.0.0.1', 8888)
# 搭建网络
s = socket()
s.connect(ADDR)

def do_register():
    while True:
        name = input("用户名：")
        passwd = getpass.getpass("密码：")
        passwd1 = getpass.getpass("请再次输入密码：")
        if passwd != passwd1:
            print("两次密码不一致！")
            continue
        if (' ' in name) or (' ' in passwd):
            print("用户名或密码不能含有空格")
            continue

        msg = ' '.join(('R', name, passwd))
        s.send(msg.encode()) # 发送请求
        data = s.recv(128).decode()  # 反馈
        if data == 'OK':
            print("注册成功")
            logined(name)
            return
        else:
            print("注册失败")
        return

def do_login():
    for i in range(3):
        name = input("用户名：")
        passwd = getpass.getpass("密码：")
        msg = ' '.join(('L', name, passwd))
        s.send(msg.encode())  # 发送请求
        data = s.recv(128).decode()  # 反馈
        if data == 'OK':
            print("登录成功\n")
            logined(name)
            return
        else:
            print("用户名或密码错误")

def query(name):
    # 查单词
    while True:
        word = input("单词(直接按回车退出)：")
        if not word:
            return
        msg = "Q %s %s"%(name, word)
        s.send(msg.encode()) # 发送请求
        mean = s.recv(2048).decode()  # 反馈
        if mean == 'error':
            print("单词不存在，请重新输入\n")
        else:
            print("单词解释：", mean, '\n')  # 单词解释



def do_hist(name):
    # 查询历史记录
    msg = "H %s" % (name)
    s.send(msg.encode())  # 发送请求
    # hist = s.recv(1024).decode()  # 反馈
    while True:
        data = s.recv(1024).decode()  # 反馈
        if data == '##':
            break
        print(data)

    # if hist == 'null':
    #     print("记录不存在\n")
    # else:
    #     for item in hist:  # 单词解释
    #         print(item)


def logined(name):
    while True:
        print("""
        ========= %s Welcome =========
        
        1.查单词   2.历史记录   3.注销
        
        =============================
        """%name)
        cmd = input("选项(1,2,3)：")
        if cmd.strip() == '1':
            query(name)
        elif cmd.strip() == '2':
            do_hist(name)
        elif cmd.strip() == '3':
            print("已注销")
            return  # 二级界面结束
        else:
            print("请输入正确命令")





def main():

    while True:
        print("""
        ========== Welcome ==========
          1.注册    2.登录    3.退出
        =============================
        """)
        cmd = input("选项(1,2,3)：")
        if cmd.strip() == '1':
            do_register()
        elif cmd.strip() == '2':
            do_login()
        elif cmd.strip() == '3':
            data = 'E'
            s.send(data.encode())
            sys.exit("系统退出")

if __name__ == '__main__':
    main()