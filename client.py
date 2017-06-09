import socket
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = '127.0.0.1'
port = 8888

s.connect((host,port))
client_name = s.recv(4096)
print('I am',str(client_name,"utf-8"))
while True:


    
    print('Please input the name of the file you want:')
    filename = input()
    s.sendall(bytes(filename,"utf-8"))
    file_object = open("Sever_"+filename,'w')

    
    print('Please choose a client which could send the file to you!')
    clients_with_file = s.recv(4096)
    print(str(clients_with_file,"utf-8"))
    choosed_client = input()
    s.sendall(bytes(choosed_client,"utf-8"))
    
    
    file_data = s.recv(4096)
    file_object.write(str(file_data,"utf8"))
    file_object.close()
    print("Successfully get the file !")
    
    

s.close()
