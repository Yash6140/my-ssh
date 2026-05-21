import socket

host='192.168.0.6' #public ip address of the server
port = 9090

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

client.send("Hi Server".encode('utf-8'))
print(client.recv(1024).decode('utf-8'))

client.close()