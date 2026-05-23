
import socket
from crypto import encrypt, decrypt
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os

KEY = os.urandom(32)  
#KEY = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff')
host='172.17.61.95' #public ip address of the server
port = 9090

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
pem_public_key = client.recv(2048)
public_key = load_pem_public_key(pem_public_key)
encrypted_key=public_key.encrypt(KEY, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
client.send(encrypted_key)

MESSAGE = "Hi Server"
client.send(encrypt(MESSAGE, KEY))
response = client.recv(2048)
#print(response)
print(decrypt(response, KEY))


client.close()