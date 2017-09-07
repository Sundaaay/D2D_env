import socket
import time
import random
import json
import os
import sys

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

def zipf():#使用户请求文件的频率满足zipf分布
    a = [1,2,3,4,5,6,7,8,9,10]#假设文件流行的排名，（可更改）
    for i in range(len(a)):
        a[i] = 1/a[i]
        if i != 0:
            a[i] = a[i] + a[i-1]
    r = random.uniform(0,a[len(a)-1])
    if r < a[0]:
        return 0
    for i in range(1,len(a)):
        if r > a[i-1] and r <= a[i] :
            return i
            break

def auto_request(client_file, all_files):
    while True:
        if random.randint(0, 9) >= 15: #设定用户需要文件的时间概率，可更改
            print('I will not send a requestion!')
            time.sleep(5)
        else:
            file_without = []#该客户端所没有的文件
            for i in range(len(all_files)):
                if client_file.count(str(all_files[i])) == 0 :
                    file_without.append(all_files[i])
            if len(file_without) == 0 :
                return False#回复False表示已拥有所有文件
                break
            
            m = zipf()
            if all_files[m] in file_without :
                filename = all_files[m]
                return filename
                break
            
            #m = random.randint(0, len(file_without)-1)#此处可更改
            else:
                print('I have ',all_files[m],',I will not send a requestion!')
                continue
            
#获取所含有文件大小       
def get_size():
    path = os.getcwd()
    for root, dirs, files in os.walk(path) :
        size = 0
    for i in range(len(files)) :
        size = size + os.path.getsize(os.getcwd()+"\\"+files[i])
    #print(size)
    size = size - os.path.getsize(sys.argv[0])
    return size

while True:
    
    #首先判断存储大小是否超过限定值
    size = get_size()
    #print(size)
    #time.sleep(60)
    while size > 2 ** 30 : #存储上限1G
        print('My files are too lot ,I have to delete some of them.')
        #每次删除一个，删除序号
        delete_number = random.randint(0,len(client_file)-1)
        #被删除的文件名称
        delete_name = client_file[delete_number]
        os.remove(delete_name)
        print('I have deleted ',delete_name)
        del client_file[delete_number]
        size = get_size()
        #print(size)
        #time.sleep(60)

        
    print('Please input the name of the file you want:')
    time.sleep(0)
    filename = auto_request(client_file, all_files)

    #当客户端拥有所有文件时，随机删除某些文件。
    if filename == False :
        print('I have all of the files !')
        print('I will delete some files.')
        #删除次数，每次删除一个
        delete_times = random.randint(1, len(client_file))
        print('delete times are',delete_times)
        for i in range(delete_times) :
            #删除序号
            delete_number = random.randint(0,len(client_file)-1)
            #被删除的文件名称
            delete_name = client_file[delete_number]
            os.remove(delete_name)
            print('I have deleted ',delete_name)
            del client_file[delete_number]   
        continue
    
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
    
    #file_object = open(choosed_name+"_"+filename,'w')
    file_object = open(filename,'w')
    file_data = s.recv(4096)
    file_object.write(str(file_data,"utf8"))
    file_object.close()
    print("Successfully get the file !")
    print('------------------------------------------------------')
    #更新自身所含文件列表，以免重复请求
    client_file.append(filename)
    
while True :
    wait = True
    

s.close()
