import socket
from crypto import encrypt, decrypt

#KEY = os.urandom(32) 
KEY = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff') 
host='172.23.153.152' #why l
#host=socket.gethostbyname(socket.gethostname())
port = 9090
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

while True:
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    encrypted_message = communication_socket.recv(1024)
    #print(f"Encrypt:{encrypted_message}")
    message = decrypt(encrypted_message, KEY)
    print(f"The message is: {message}")
    communication_socket.send(encrypt("Server has received the message", KEY))
    communication_socket.close()
    print("Connection closed")

