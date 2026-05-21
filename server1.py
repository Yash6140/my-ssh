import socket
host='192.168.0.6' #why l
#host=socket.gethostbyname(socket.gethostname())
port = 9090
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

while True:
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    message = communication_socket.recv(1024).decode('utf-8')
    print(f"The message is: {message}")
    communication_socket.send("Server has received the message".encode('utf-8'))
    communication_socket.close()
    print("Connection closed")

