# Monica Dimitrova
# 2135425
# Sept. 23rd, 2023
# This program is a socket server that handles incoming client connections,
# and authenticate clients.



#from threading import Thread
import socket
import threading
import mqtt.jwt as jwt
import datetime


# get the hostname (if client and server is in the same Host for testing purposes)
host = socket.gethostname()
#If you connect from a different host, change to your IP (or hostname if you are using DNS)
#host = '192.168.0.132'

PORT = 15788  # initiate port number above 1024
SERVER = socket.gethostbyname(socket.gethostname())
'''
If server is behind a firewall, you need to add the port, example with ufw:
sudo ufw allow 15789
'''


ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
    


def handle_client(conn, addr):
    print(f"NEW CONNECTION: {addr}")

    connected = True
    while connected:
        #conn, addr = server.accept()  # accept new connection
        # receive data stream. it won't accept data packet greater than 1024 bytes
        conn.send(f"I am the server accepting connections on port {PORT}...".encode())

        data = conn.recv(1024).decode("utf-8")
        dataArray = data.split(",")
        
        token = authenticate(dataArray[0], dataArray[1])
        if token is None:
            errorConnecting = "Error connecting"
            conn.send(errorConnecting.encode("utf-8"))
        else:
            conn.send(token)
            print(f"{addr} successfully authenticated")
            #-1 to not count the server
            print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")
             
    conn.close()



SECRET = "my-secret"

def authenticate(username, password):
    if username == "admin" and password == "password":
        # Create a JWT token with a subject claim "admin" and an expiration time of 1 hour
        #expire_on = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        expire_on = datetime.datetime.utcnow() + datetime.timedelta(seconds=0.5)
        payload = {"sub": "admin", "exp": expire_on.timestamp()}
        token = jwt.encode(payload, SECRET, algorithm="HS256")
        return token
    else:
        return None
    

def start():
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() #accept new connection
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=False)
        thread.start()
       
        
print("SERVER IS STARTING")
start()
        

# data = input(' -> ')
        