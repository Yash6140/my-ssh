# my-ssh
##Working mechanism: 
A raw TCP connection is established between the client and server.
The server sends its RSA-2048 public key to the client. The client generates a fresh 32-byte session key using os.urandom(32), encrypts it with the server's public key via RSA-OAEP, and sends it back. The server decrypts it with its private key. The session key is now a shared secret 
All subsequent communication is encrypted with AES-GCM using this session key combining the security of asymmetric RSA for key exchange with the speed of symmetric AES for bulk data transfer (hybrid encryption).
The client stores its RSA public key to the json file. The server uses it to verify the digital signature of the client 
The server sends a challenge to the client, which it signs with its private key using RSA-PSS and sends the signature back. The server verifies it against the stored public key.
Only after the signature is verified does the shell loop begin every command typed by the client and every response from the server travels as AES-GCM ciphertext over the wire.
##Learnings:
#TCP model-> guarantees ordered, reliable delivery of bytes. IP handles routing between machines.
#AES-GCM -> encrypts data with a shared secret key and simultaneously produces an authentication tag, i.e meaning the receiver can verify the message wasn't tampered with in transit. It requires a unique nonce per message.
RSA is asymmetric — anything encrypted with the public key can only be decrypted with the private key, and anything signed with the private key can be verified with the public key. This is what makes key exchange and authentication possible.
Hybrid encryption combines both: RSA to securely exchange a symmetric key, then AES-GCM for everything after.
#Digital Signatures -> The client signs the server's random challenge with its private key; the server verifies with the stored public key. A valid signature proves key possession without the private key ever leaving the client.
Essentially, the challenge is summarised using a hash function, which is then encrypted.
RSA-PSS adds randomness to signing so the same message signed twice produces different signatures, preventing replay and pattern attacks.
