import os
import random
import socket
import threading
import time

from trans_file import trans_file_Client, trans_file_Server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8888
position = (1234, 5678)
client.connect((host, port))
FILE_DIR = 'F:/Client'

def package(message, size):
    new_message = message
    while len(bytes(new_message, 'utf-8')) < size:
        new_message = new_message + '-'
    return new_message


def generate_position():
    """
    generate the client`s position
    :return: postion like (x, y)
    """
    position = (random.uniform(1, 200), random.uniform(1, 200))
    return position


def list_append(choose_list, j):
    for i in choose_list:
        if j == i:
            return
    choose_list.append(j)


def show_file_inf():
    choose_list = list()
    recv_file_data = client.recv(1024)
    data = str(recv_file_data, 'utf-8').rstrip('-')
    print(data)
    recv_file_dict = eval(data)     # 将字典的字符串转化成字典
    for i, j in recv_file_dict.items():
        print('{}里的文件有: '.format(i), end='')
        for m in j:
            if m == '':
                continue
            print('{}    '.format(m), end='')
            list_append(choose_list, m)
        print('\n')
    print('*' * 20)
    return choose_list


def choose_file(choose_list, file_dir):
    random_num = random.randint(0, len(choose_list) - 1)
    while choose_list[random_num] in file_dir:
        if len(choose_list) == len(file_dir):
            return -1
        print('you had the file in you directory please rechoose!')
        random_num = random.randint(0, len(choose_list) - 1)
    return choose_list[random_num]


def request():
    while True:

        # 请求的概率是无法确定的，所以我先采用的是概率为50%，即每个客户端到这里都有50%的概率会随机请求一个文件
        if random.randint(0, 9) >= 5:
            print('i will not send a request!')
            time.sleep(5)
            continue

        # 生成client所在的位置信息
        position = generate_position()
        client.sendall(bytes(package(str(position), 1024), 'utf-8'))
        print('sended position...')
        print('*' * 20)

        # 读取该文件夹下的文件,将文件列表发送至服务器
        file_dir = os.listdir(FILE_DIR)
        client.sendall(bytes(package('$'.join(file_dir), 1024), 'utf-8'))
        print('sended file_dir...')
        print('*' * 20)

        # 接收来自服务器的包含文件信息的字典显示出来  这里你可能改成命名元组或者其他
        choose_list = show_file_inf()

        # 随机选择一个文件进行传输,
        print('可以选择的文件有{}'.format(choose_list))
        random_file = choose_file(choose_list, file_dir)
        if random_file == -1:                                               # 返回 -1 表示该节点中已经拥有了所有节点的文件了
            client.sendall(bytes(package('have_all_file', 1024), 'utf-8'))
            print('contained all file in the system!')
            continue
        client.sendall(bytes(package(random_file, 1024), 'utf-8'))

        print('*' * 20)

        # 3、服务器向客户端返回所有包含这个文件的节点信息的一个列表
        best_sender = str(client.recv(1024), 'utf-8').rstrip('-')
        if best_sender == '404':
            print('this file is not in this System!')
            continue
        else:
            print('the best sender is {}'.format(best_sender))
            fp = open(FILE_DIR+'/'+random_file, "w")
            fp.close()
        print('*' * 20)


thread_request = threading.Thread(target=request(), args=())
thread_request.start()
client.close()
