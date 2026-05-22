import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(message, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)       
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)
    return nonce + ciphertext     # send nonce along with the ciphertext

def decrypt(data, key):
    aesgcm = AESGCM(key)
    nonce = data[:12]             
    ciphertext = data[12:]        
    return aesgcm.decrypt(nonce, ciphertext, None).decode()