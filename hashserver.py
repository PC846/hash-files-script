import socket
import threading
import pickle
import sys

#check to see if port is given
arg_list = sys.argv[1:]
if arg_list and len(arg_list) == 1:
    arg_list[0] = int(arg_list[0])
    PORT = arg_list[0]
else:
    PORT = 2345

#accept any IP address
SERVER = '0.0.0.0'

ADDR = (SERVER, PORT)

#opening data flow and binding
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#handles different clients connecting to the server
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while 1:
        data = conn.recv(4096) #recieve data
        if not data:
            break
        else:
            conn.send(data) #sends the data back to the client
    conn.close()
        
#starts the server
def start():
    server.listen(1)
    print(f"[SERVER STARTED ON...{PORT}]")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #starts a thread for each connect client
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # -1 since it includes the thread the server/client is running on

print("[STARTING] server is starting...")
start()