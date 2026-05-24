import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(message_bytes, key): #takes a string message 
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)       
    ciphertext = aesgcm.encrypt(nonce, message_bytes, None)
    return nonce + ciphertext     # send nonce along with the ciphertext

def decrypt(data, key): #takes a bytestream 
    aesgcm = AESGCM(key)
    nonce = data[:12]             
    ciphertext = data[12:]        
    return aesgcm.decrypt(nonce, ciphertext, None)