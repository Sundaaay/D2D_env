import socketserver
import json
import time
import os
import datetime
i = 0

# 所有可传送的文件名


data = {}

# # 传送文件历史记录
# trans_data = {}

# 位置信息
all_client_position = []

# 存储所有的文件夹所在的位置
FILE_DIR = os.getcwd()+'/server_dir'  # '/home/ry/桌面/D2D_env-zhao_V-2/Server/server_dir'


def get_all_file():
    file_list = os.listdir(FILE_DIR)
    return file_list

# 所有客户端所拥有的文件的字典
all_files = get_all_file()

# 产生位置信息的函数，返回值为所有客户端的位置信息
def product_position(all_client):
        all_client_position = []
        
        for m in range(len(all_client)):
                positon = (m, m)
                all_client_position.append(positon) 

        time.sleep(2)
        return all_client_position


def find_the_best_client(clients_with_file, all_client_position, all_client, client_name):
        if len(clients_with_file) == 0:
                choosed_name = 'basestation'
                return choosed_name
        else:
                clients_with_file_positon = []
                instance = []
                 # 确定请求传送文件的客户端的位置
                temp = all_client.index(client_name)
                client_name_positoin = all_client_position[temp]

                # 确定所有拥有指定文件的客户端的位置
                for n in range(len(clients_with_file)):
                        temp = all_client.index(clients_with_file[n])
                        clients_with_file_positon.append(all_client_position[temp])

                for m in range(len(clients_with_file)):
                        length = (clients_with_file_positon[m][0] - client_name_positoin[0])**2 + (clients_with_file_positon[m][1] - client_name_positoin[1])**2
                        instance.append(length)
                temp = instance.index(min(instance))
                choosed_name = clients_with_file[temp]
                print(clients_with_file, instance)
                return choosed_name


def write_history(source_host, target_host, filename):
    pwd = os.getcwd()
    hisotory_file = open(os.getcwd()+'/history', 'a')
    cur_time = str(time.time())
    hisotory_file.write('time:{}\tsource_host:{}\ttaget_host:{}\ttrans_file:{}\t\n'.format(cur_time, source_host, target_host, filename))
    hisotory_file.close()


class myTCPHandler(socketserver.BaseRequestHandler):
        
        def handle(self):
                
                clients = []  # 已连接客户端名称
                
                # 拥有指定文件的客户端列表，默认基站拥有全部文件
                clients_with_file = []
                global i

                # 最新连接的客户端代号，如C1 , C2
                client_name = 'C'+str(i)

                # 第一次发送
                self.request.sendall(bytes(client_name, encoding="utf8"))
                i += 1
                clients.append(client_name)
                print('get connection from', self.client_address, 'as', client_name, data)

                while 1:
                        '''
                        首先说一下将前面的过程移动到这里的原因：
                        1、客户端在接收到文件后，它的信息就变了，就要进行跟新,每次传输过后就跟新一次。
                        这里去掉第二次发送列表到客户端，转而由客户端发送过来。
                        '''
                        # 第一点五次接收客户端发送过来的文件
                        self.data = self.request.recv(1024)
                        client_file = json.loads(str(self.data, encoding='utf-8'))
                        data[client_name] = tuple(client_file)
                        print('{} have {}'.format(client_name, client_file))

                        # 第二次发送,将client_file发给客户端
                        # self.request.sendto(json.dumps(client_file).encode(), (h, p))

                        # 第三次发送，将all_files发给客户端
                        all_files_list = list(all_files)
                        self.request.sendto(json.dumps(all_files).encode(), (h, p))
                        # 第一次接收
                        self.data = self.request.recv(1024)
                        filename = str(self.data, encoding="utf-8")

                        # 寻找哪些客户端含有指定文件
                        all_client = list(data.keys())
                        for m in range(len(all_client)):
                            for n in range(len(data[all_client[m]])):
                                if all_client[m] == client_name:
                                        continue
                                if data[all_client[m]][n] == filename:
                                        clients_with_file.append(all_client[m])

                        # 获取所有主机的位置信息
                        all_client_position = product_position(all_client)

                        choosed_name = find_the_best_client(clients_with_file, all_client_position, all_client, client_name)

                        print(choosed_name, 'will send', filename, 'to', client_name)
                        # 第四次发送
                        self.request.sendall(bytes(str(choosed_name), encoding="utf8"))
                        file_object = open(FILE_DIR+'/'+filename)
                        try:
                                file_data = file_object.read()
                        finally:
                                file_object.close()
                        print(choosed_name, 'has send', filename, 'to', self.client_address, client_name)
                        self.request.sendall(bytes(file_data, encoding="utf8"))
                        # 更新data字典
                        data[client_name] = data[client_name]+tuple([filename])
                        # 显示更新后的data字典
                        # print(data[client_name])
                        '''
                        这里去掉原来的在服务端进行传输情况的打印，将历史写入一个文件中。
                        '''
                        write_history(choosed_name, client_name, filename)

                        # if choosed_name in trans_data.keys():
                        #         trans_data[choosed_name] = trans_data[choosed_name] + tuple([client_name,filename])
                        # else:
                        #         trans_data[choosed_name] = tuple([client_name, filename])
                        print('------------------------------------------------------')

                        # 重置该列表，以便下次使用
                        clients_with_file = []
                        

h, p = '0.0.0.0', 9999
server = socketserver.ThreadingTCPServer((h, p), myTCPHandler)
server.serve_forever()

