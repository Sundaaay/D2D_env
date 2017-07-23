import socket
import time
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 8888
position = (1234, 5678)
client.connect((host, port))


def package(message,size):
    new_message = message
    while len(bytes(new_message, 'utf-8')) < size:
        new_message = new_message + '-'
    return new_message


while True:
    # 1、读取该文件夹下的文件,将文件列表发送至服务器
    file_dir = os.listdir('F://Client')
    client.sendall(bytes(package('$'.join(file_dir), 1024), 'utf-8'))
    print('sended file_dir!')

    # 接收来自服务器的包含文件信息的字典显示出来  这里你可能改成命名元组或者其他
    recv_file_data = client.recv(1024)
    data = str(recv_file_data, 'utf-8').rstrip('-')
    recv_file_dict = eval(data)
    for i, j in recv_file_dict.items():
        print('{}里的文件有: '.format(i), end='')
        for m in j:
            print('{}    '.format(m), end='')
        print('\n')
    print('*' * 20)

    # 2、用户输入想获取的文件
    filename = input('Please input the name of the file you want:')

    client.sendall(bytes(package(filename, 1024), 'utf-8'))

    print('*' * 20)

    # 3、服务器向客户端返回所有包含这个文件的节点信息的一个列表
    contain_file_list = str(client.recv(1024), 'utf-8').rstrip('-').split('$')
    print(contain_file_list)
    for i in contain_file_list:
        print('{}----{}'.format(contain_file_list.index(i), i))
    print('*'*20)

    # 4、用户选择一个节点在列表中的下标
    choosed_client = int(input('Please choose a client which could send the file to you:'))
    client.sendall(bytes(package(contain_file_list[choosed_client], 60), "utf-8"))
    print("Successfully get the file !")

s.close()
