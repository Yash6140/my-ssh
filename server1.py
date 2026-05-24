import socket
from crypto import encrypt, decrypt
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives import serialization as serialisation
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json,os

privatekey= rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key=privatekey.public_key()

pem_public_key =public_key.public_bytes(
  encoding=serialisation.Encoding.PEM,
  format=serialisation.PublicFormat.SubjectPublicKeyInfo
)



#KEY = os.urandom(32) 
#KEY = bytes.fromhex('00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff') 

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
    print("Received encrypted key (AES)")

    challenge= os.urandom(32)
    communication_socket.sendall(encrypt(challenge, aes_gcm_key))
    
    print("sent challenge")
    

    with open("authorised_keys.json", "r") as json_file:
      loaded_data = json.load(json_file)

    
    public_key_string = loaded_data["public_key"]
    public_key = serialisation.load_pem_public_key(public_key_string.encode('utf-8'))  #usable format(raw py object) for encryption (not string)

    received_signature = communication_socket.recv(2048)

    print("JSON data loaded successfully")

    try:
      public_key.verify(received_signature,challenge,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
      print("Authentication Successful!")
      communication_socket.send(encrypt(b"AUTH_SUCCESS", aes_gcm_key))

      
      encrypted_message = communication_socket.recv(2048)
      #print(f"Encrypt:{encrypted_message}")
      message = decrypt(encrypted_message, aes_gcm_key)
      print(f"The message is: {message.decode('utf-8')}")
      message2="Server has received the message"
      communication_socket.send(encrypt(message2.encode('utf-8'), aes_gcm_key))
      communication_socket.close()
      print("Connection closed")
      
    except Exception as e:
      print(f"Authentication Failed! {repr(e)}")
      communication_socket.send(encrypt(b"AUTH_FAILED", aes_gcm_key))
      communication_socket.close()






