import socket
from crypto import encrypt, decrypt
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives import serialization as serialisation
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

privatekey= rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key=privatekey.public_key()

pem_public_key =public_key.public_bytes(
  encoding=serialisation.Encoding.PEM,
  format=serialisation.PublicFormat.SubjectPublicKeyInfo
)



#KEY = os.urandom(32) 
KEY = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff') 
#host='172.23.153.152'
host=socket.gethostbyname(socket.gethostname())
port = 9090
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

while True:
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    communication_socket.sendall(pem_public_key)
    encrypted_key=communication_socket.recv(2048)
    aes_gcm_key=privatekey.decrypt(encrypted_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print(f"Received encrypted key: {encrypted_key.hex()}")
    encrypted_message = communication_socket.recv(2048)
    #print(f"Encrypt:{encrypted_message}")
    message = decrypt(encrypted_message, aes_gcm_key)
    print(f"The message is: {message}")
    communication_socket.send(encrypt("Server has received the message", aes_gcm_key))
    communication_socket.close()
    print("Connection closed")

