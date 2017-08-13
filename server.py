import os
import socketserver
import threading


file_dict = {}
host_position = {}
BASE_LOCALHOST = '0.0.0.0'
BASE_POSITION = (34, 56)
FILE_DIR = 'F:/Server'
HISTORY_DIR = 'F:/file_tans_history.txt'


def package(message, size):
    new_message = message
    while len(bytes(new_message, 'utf-8')) < size:
        new_message = new_message + '-'
    return new_message


def find_file_host(file_dict, filename, client_address):
    host_list = list()
    for i, j in file_dict.items():
        for m in j:
            if m == filename and i != client_address:
                host_list.append(i)
    return host_list


def choose_best_sender(host_position, host_have_the_file, request_ip):
    if len(host_have_the_file) == 0:
        print('there is not the file in the System!')
        return -1
    p1 = host_position[request_ip]
    distance_dict = dict()
    for name in host_have_the_file:
        p = host_position[name]
        distance_dict[name] = (pow(p1[0] - p[0], 2) + pow(p1[1] - p[1], 2)) ** 0.5
    best_host = host_have_the_file[0]
    for name, dis in distance_dict.items():
        if dis <= distance_dict[best_host]:
            best_host = name
    print('the best sender is {}'.format(best_host))
    return best_host


def write_trans_history(req_host, send_host, file_name):
    fp = open(HISTORY_DIR, 'a')
    fp.write(send_host + ':' + str(host_position[send_host]) + '-->' + req_host + ':' + str(
        host_position[req_host]) + ':' + file_name + '\n')
    fp.close()


class myTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while 1:
            # 从本地读取某一个文件夹中的文件数据当作基站所拥有的文件
            file_list = os.listdir(FILE_DIR)
            file_dict[BASE_LOCALHOST] = tuple(file_list)
            host_position[BASE_LOCALHOST] = BASE_POSITION

            # 0、接收客户端发送过来的位置信息，保存到 host_position字典中
            client_data = self.request.recv(1024)
            data = str(client_data, 'utf-8').rstrip('-')
            host_position[self.client_address[0]] = eval(data)
            for i, j in host_position.items():
                print('{}:{}\n'.format(i, j))

            # 1、接收客户端发送过来的文件列表,添加到file_dict字典中
            client_data = self.request.recv(1024)
            print('receive file_dict from client:{}'.format(self.client_address))
            data = str(client_data, 'utf-8').rstrip('-')
            client_file_list = data.split('$')
            file_dict[self.client_address[0]] = tuple(client_file_list)
            print('update file_dict!')
            for i, j in file_dict.items():
                print('{} 里的文件有: '.format(i), end='')
                for m in j:
                    print('{}    '.format(m), end='')
                print('\n')
            print('*' * 20)

            # 2、将服务器中的file_dict 发送发客户端 因为字典转换成字符串后在客户端无法将这个字符串转换成字典
            self.request.sendall(bytes(package(str(file_dict), 1024), 'utf-8'))
            print('sended file_dict to Client:  {}...'.format(self.client_address[0]))
            print('*' * 20)

            # 3、接收客户端发来的所请求的文件名
            filename_data = self.request.recv(1024)
            req_filename = str(filename_data, 'utf-8').rstrip('-')
            if req_filename == 'have_all_file':
                continue
            print('client:  {} choose a file:  {}'.format(self.client_address[0], req_filename))
            print('*' * 20)

            # 4、在file_dict 的 value中查找这个文件，返回一个有这个文件的主机的ip 的列表
            host_have_the_file = find_file_host(file_dict, req_filename, self.client_address[0])

            # 在包含了该文件的主机列表中选择，距离请求主机最近的主机作为最优文件发送者
            best_sender = choose_best_sender(host_position, host_have_the_file, self.client_address[0])

            # 如果该系统中没有这个文件就返回 404 错误，若有就将这个主机发送给请求主机。
            if best_sender == -1:
                print('find file error 404 !')
                self.request.sendall(bytes(package('404', 1024), 'utf-8'))
                continue
            else:
                self.request.sendall(bytes(package(best_sender, 1024), 'utf-8'))
            write_trans_history(self.client_address[0], best_sender, req_filename)


def deal_request():
    h, p = '', 8888
    server = socketserver.ThreadingTCPServer((h, p), myTCPHandler)
    server.serve_forever()


thread_del_request = threading.Thread(target=deal_request(), args=())
thread_del_request.start()

