import socketserver
import socket
import os

data = {}
trans_data = {}
file_dict = {}


def package(message, size):
    new_message = message
    while len(bytes(new_message, 'utf-8')) < size:
        new_message = new_message + '-'
    return new_message


def find_file_host(file_dict, filename):
        host_list = list()
        for i, j in file_dict.items():
                for m in j:
                        if m == filename:
                                host_list.append(i)
        return host_list

def add_file(file_dict, file_send_host, req_filename):
        for i in file_dict[file_send_host]:
                if req_filename == i:
                        return
        file_dict[file_send_host] = tuple(list(file_dict[file_send_host]).append(req_filename))


class myTCPHandler(socketserver.BaseRequestHandler):
        
        def handle(self):
                while 1:
                        # 从本地读取某一个文件夹中的文件数据当作基站所拥有的文件
                        file_list = os.listdir('F://Server')
                        file_dict[socket._LOCALHOST] = tuple(file_list)

                        # 1、接收客户端发送过来的文件列表,添加到file_dict字典中
                        client_data = self.request.recv(1024)
                        print('receive file_dict from client:{}'.format(self.client_address))
                        data = str(client_data, 'utf-8').rstrip('-')
                        client_file_list = data.split('$')
                        file_dict[self.client_address[0]] = tuple(client_file_list)
                        print('update file_dict!')
                        for i, j in file_dict.items():
                                print('{}里的文件有: '.format(i), end='')
                                for m in j:
                                        print('{}    '.format(m), end='')
                                print('\n')
                        print('*'*20)

                        # 2、将服务器中的file_dict 发送发客户端 因为字典转换成字符串后在客户端无法将这个字符串转换成字典
                        self.request.sendall(bytes(package(str(file_dict), 1024), 'utf-8'))
                        print('sended file_dict to Client!')
                        print('*'*20)

                        # 3、接收客户端发来的所请求的文件名
                        filename_data = self.request.recv(1024)
                        req_filename = str(filename_data, 'utf-8').rstrip('-')
                        print('cilent choose a file:  {}'.format(req_filename))
                        print('*'*20)

                        # 4、在file_dict 的 value中查找这个文件，返回一个有这个文件的主机的ip 的列表
                        host_have_thefile = find_file_host(file_dict, req_filename)

                        # 5、将这个主机列表发送给请求的客户机
                        self.request.sendall(bytes(package('$'.join(host_have_thefile), 1024), 'utf-8'))

                        # 6、接收客户选择的主机
                        file_send_host = str(self.request.recv(60), 'utf-8').rstrip('-')
                        print(file_send_host)

                        add_file(file_dict, file_send_host, req_filename)

                        

h,p = '', 8888
server = socketserver.ThreadingTCPServer((h,p),myTCPHandler)
server.serve_forever()
