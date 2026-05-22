
import socket
from crypto import encrypt, decrypt

#KEY = os.urandom(32)  
KEY = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff')
host='172.23.153.152' #public ip address of the server
port = 9090

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
MESSAGE = "Hi Server"

client.send(encrypt(MESSAGE, KEY))
response = client.recv(1024)
#print(response)
print(decrypt(response, KEY))


client.close()