import socketserver

i=0



data = {}

trans_data = {}
class myTCPHandler(socketserver.BaseRequestHandler):
        
        def handle(self):
                
                clients = []
                clients_with_file = ['base_station']
                global i
                
                client_name = 'C'+str(i)
                self.request.sendall(bytes(client_name ,encoding = "utf8"))
                
                client_file = ('file'+str(i)+'.txt','file'+str(i+1)+'.txt','file'+str(i+2)+'.txt')
                
                data[client_name] = client_file
                i += 1
                
                clients.append(client_name)
                print('get connection from',self.client_address,'as',client_name,data)
                while 1:
                        self.data = self.request.recv(1024)
                        filename = str(self.data,encoding = "utf-8")
                        
                        

                        
                        keys = list(data.keys())
                        for m in range(len(keys)):
                            for n in range(len(data[keys[m]])):
                                if keys[m] == client_name:
                                        continue
                                if data[keys[m]][n] == filename:
                                    clients_with_file.append(keys[m])

                        
                        self.request.sendall(bytes(str(clients_with_file),encoding = "utf8"))
                        self.data = self.request.recv(1024)
                        
                        
                        choosed_name = str(self.data,encoding = "utf-8")
                                 
                        file_object = open(filename)
                        try:
                                file_data = file_object.read( )
                        finally:
                                file_object.close( )
                        print (choosed_name,'has send',filename,'to',self.client_address,client_name)
                        self.request.sendall(bytes(file_data ,encoding = "utf8"))

                        
                        if choosed_name in trans_data.keys():
                                trans_data[choosed_name] = trans_data[choosed_name] + tuple([client_name,filename])
                        else:
                                trans_data[choosed_name] = tuple([client_name,filename])
                        print("The historical information:",trans_data)

                       
                        clients_with_file = ['base_station']
                        

h,p = '',8888
server = socketserver.ThreadingTCPServer((h,p),myTCPHandler)
server.serve_forever()
