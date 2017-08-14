import socket
import time
import random
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    

host = '127.0.0.1'
port = 8888

s.connect((host,port))

#第一次接收，客户端名称
client_name = s.recv(4096)
print('I am',str(client_name,"utf-8"))

#第二次接收，该客户端含有文件列表,该client_file类型为列表
client_file = json.loads(str(s.recv(4096),"utf-8"))
print('I have ',client_file)
#print(type(client_file))

#第三次接收，所有文件名
all_files = json.loads(str(s.recv(4096),"utf-8"))
print('All of the files are ',all_files)

def auto_request(client_file, all_files):
    while True:
        if random.randint(0, 9) >= 15: 
            print('I will not send a requestion!')
            time.sleep(5)
        else:
            file_without = []#该客户端所没有的文件
            for i in range(len(all_files)):
                if client_file.count(str(all_files[i])) == 0 :
                    file_without.append(all_files[i])
            if len(file_without) == 0 :
                return False
                break
            
            m = random.randint(0, len(file_without)-1)#此处可更改
            filename = file_without[m]
            return filename

while True:

    
    print('Please input the name of the file you want:')
    time.sleep(5)
    filename = auto_request(client_file, all_files)
    if filename == False :
        print('I have all of the files !')
        break
    print('I want ', filename)
    #filename = input()

    #第一次发送，文件名
    s.sendall(bytes(filename,"utf-8"))
    
    
    #print('Please choose a client which could send the file to you!')
    
    #第四次接收，发送端名称
    choosed_name = str(s.recv(4096),"utf-8")
    print(choosed_name,'will send',filename,'to me.')
    #choosed_client = input()
    #s.sendall(bytes(choosed_client,"utf-8"))
    
    file_object = open(choosed_name+"_"+filename,'w')
    file_data = s.recv(4096)
    file_object.write(str(file_data,"utf8"))
    file_object.close()
    print("Successfully get the file !")

    #更新自身所含文件列表，以免重复请求
    client_file.append(filename)
    
while True :
    wait = True
    

s.close()
