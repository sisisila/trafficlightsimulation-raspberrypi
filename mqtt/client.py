# Monica Dimitrova
# 2135425
# Sept. 23rd, 2023
# This acts as a client to connect to the server, over a socket connection.


import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    #If you connect from a different host, change to your IP (or hostname if you are using DNS)
    #host = '192.168.0.132'
    port = 15788  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    print('Connected to host '+str(host)+' in port: '+str(port))
    message = client_socket.recv(1024)
    print("Message from the server: ", message.decode("utf-8"))
    

    #while message.lower().strip() != 'quit':
    while True:
        messageOne = input("Username:")  # take input
        messageTwo = input("Password:")  # take input
        message = messageOne + "," + messageTwo
        client_socket.send(message.encode("utf-8"))  # send message

        token = client_socket.recv(1024).decode("utf-8")  # receive response
        if token == "Error connecting":
            print("Did not connect successfully. Try again!")
        else:
            break

        print('Received from server: ' + token)  # show in terminal
        if message.lower().strip() == 'quit':
            break

        
        
    while message.lower().strip() != 'quit':
        message = input(" -> ")


    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()