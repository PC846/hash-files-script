
import socket
import sys
import hashlib
from IPy import IP
import re
import pickle
import string

#handles optional argument
arg_list  = sys.argv[1:]

if len(arg_list[0]) > 5: #checks for port number
    PORT = 2345
    SERVER = arg_list[0]
elif arg_list[0].isdigit(): #otherwise assume its the IP
    if len(arg_list[0]) <= 5 and IP(arg_list[0]):
        PORT = int(arg_list[0])
        SERVER = arg_list[1]
        arg_list = arg_list[1:]
    else:
        raise ValueError("[INVALID IP ADDRESS]")

#connecting and binding
ADDR = (SERVER, PORT)
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print(f"[CONNECTED]...{ADDR}")


#sends data and receive hashed data to be sent to the server
def send(sdata):
    hash_name = sdata[1] 
    hash_list = find_files(sdata, hash_name)
    data_str = pickle.dumps(hash_list)
    client.send(data_str)

    data = client.recv(4096)
    data_arr = pickle.loads(data)
    for x,y in zip(*data_arr):
        x_formatted = format(x, "<35")
        print(x_formatted, y)

    client.close()
#adds all the files in a list to be hashed       
def find_files(arg_list, hash_name):
    file_list = []
    
    for i in arg_list:
        if re.search('\.([A-Za-z]*$)',i): #handles all file extensions
            file_list.append(i)
    hash_list = hash(file_list,hash_name)
    return(hash_list,file_list)

#hashes the files and appends them into a list to be sent to the server
def hash(f_list, hash_name):
    hash_list = []
    
    if hash_name == "sha512":
        print("[OK]...sha512")
        for hash in f_list:
            result = hashlib.sha512(hash.encode())
            result = result.hexdigest()
            hash_list.append(result)
    elif hash_name == "sha1":
        print("[OK]...sha1")
        for hash in f_list:
            result = hashlib.sha1(hash.encode())
            result = result.hexdigest()
            hash_list.append(result)  

    elif hash_name == "sha256":
        print("[OK]...sha256")
        for hash in f_list:
            result = hashlib.sha256(hash.encode())
            result = result.hexdigest()
            hash_list.append(result)  
    
    elif hash_name == "md5":
        print("[OK]...md5")
        for hash in f_list:
            result = hashlib.md5(hash.encode())
            result = result.hexdigest()
            hash_list.append(result)
    else:
        print("[ERROR]...INVALID HASH NAME")  


    return(hash_list)
    
send(arg_list)
