import socket

from cryptography.hazmat.primitives import serialization
from crypto import encrypt, decrypt
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os
from cryptography.hazmat.primitives.asymmetric import rsa
import json



KEY = os.urandom(32)  
#KEY = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff')
host='172.23.153.152' #public ip address of the server
port = 9090

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = client_private_key.public_key()
pem_client_public_key=public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
pem_client_private_key=client_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)



public_key_string=pem_client_public_key.decode('utf-8')



json_data = {
    "client_id": "client_1",
    "public_key": public_key_string
} 

with open("authorised_keys.json", "w") as json_file: #w = write mode 
    json.dump(json_data, json_file, indent=4)


client.connect((host,port))
pem_public_key = client.recv(2048)
public_key = load_pem_public_key(pem_public_key)
encrypted_key=public_key.encrypt(KEY, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
client.send(encrypted_key)


encrypted_challenge = client.recv(2048)
challenge = decrypt(encrypted_challenge, KEY)#
signature = client_private_key.sign(
    challenge,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)
print("Challenge signed successfully")
client.send(signature)

response = client.recv(2048)
response=decrypt(response, KEY)
if response == b"AUTH_SUCCESS":
    while True: 
        command= input("Enter a command: ")
        if command.lower() == "exit":
            client.sendall(b"Exit")
            break
        if command=="ls":
            command="dir"
        elif command=="pwd":
            command="cd"
        
        encrypted_command=encrypt(command.encode('utf-8'), KEY)
        client.sendall(encrypted_command)
        response = client.recv(2048)
        response=decrypt(response, KEY).decode('utf-8')
        print(f"Response from server: {response}")
    client.close()
else:
    print("Connection closed by the server!")
    client.close()






