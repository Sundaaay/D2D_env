import socketserver

i=0


#存储客户端与其拥有文件的字典
data = {}
#存储文件传输记录（若必要，可将该字典改为文件）
trans_data = {}
class myTCPHandler(socketserver.BaseRequestHandler):
        
        def handle(self):
                #假设基站拥有所有文件
                clients = []
                clients_with_file = ['base_station']
                global i
                #客户端代号
                client_name = 'C'+str(i)
                self.request.sendall(bytes(client_name ,encoding = "utf8"))
                #客户端拥有的文件名（可改）
                client_file = ('file'+str(i)+'.txt','file'+str(i+1)+'.txt','file'+str(i+2)+'.txt')
                
                data[client_name] = client_file
                i += 1
                #客户端名称列表
                clients.append(client_name)
                print('get connection from',self.client_address,'as',client_name,data)
                while 1:
                        self.data = self.request.recv(1024)
                        filename = str(self.data,encoding = "utf-8")
                        
                        #加入距离判断

                        #选择客户端
                        keys = list(data.keys())
                        for m in range(len(keys)):
                            for n in range(len(data[keys[m]])):
                                if keys[m] == client_name:
                                        continue
                                if data[keys[m]][n] == filename:
                                    clients_with_file.append(keys[m])

                        #print(str(clients_with_file))
                        self.request.sendall(bytes(str(clients_with_file),encoding = "utf8"))
                        self.data = self.request.recv(1024)
                        
                        #被客户端选中发送端代号
                        choosed_name = str(self.data,encoding = "utf-8")
                        #发送文件          
                        file_object = open(filename)
                        try:
                                file_data = file_object.read( )
                        finally:
                                file_object.close( )
                        print (choosed_name,'has send',filename,'to',self.client_address,client_name)
                        self.request.sendall(bytes(file_data ,encoding = "utf8"))

                        #将文件发送的源与目的地存入,并打印
                        if choosed_name in trans_data.keys():
                                trans_data[choosed_name] = trans_data[choosed_name] + tuple([client_name,filename])
                        else:
                                trans_data[choosed_name] = tuple([client_name,filename])
                        print("The historical information:",trans_data)

                        #将该列表复原，以便下次传输文件使用
                        clients_with_file = ['base_station']
                        

h,p = '',8888
server = socketserver.ThreadingTCPServer((h,p),myTCPHandler)
server.serve_forever()
