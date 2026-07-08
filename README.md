 Build Your Own SSH

A small project where I tried to build the core ideas behind SSH from scratch , just using raw TCP sockets and basic cryptography, no existing SSH libraries.

## What it does

Two programs, a client and a server talk to each other over TCP, and I gradually made the connection more secure in stages:

1. **Plain TCP** — client and server just send messages to each other. No encryption. I checked with Wireshark and could see the message in plaintext, which was the whole problem I wanted to fix.
2. **AES-GCM encryption** — messages are now encrypted with a shared key before sending. Wireshark now shows unreadable ciphertext instead of plaintext.
3. **RSA key exchange** — instead of hardcoding the key, the server sends its public key, and the client uses it to securely send over a random session key (RSA-OAEP).
4. **Authentication** — the client has its own keypair too. The server sends a random challenge, the client signs it (RSA-PSS), and the server checks the signature before allowing access.
5. **Remote shell** — once authenticated, the client can send basic commands (`whoami`, `ls`, `pwd`) and get encrypted output back from the server.

## Rules I set for myself

- No high-level libraries like `paramiko` or `asyncssh`  only raw sockets and basic crypto primitives
- Had to actually understand TCP/sockets, not just call an API
- Commit after finishing each stage, so progress is visible in the commit history

## Tech used

- Python (sockets, `cryptography` library for AES/RSA)
- Wireshark for verifying encryption at each stage

## Running it

```bash
python server.py
python client.py
```

## Notes

This was mainly a learning project to understand networking and cryptography basics. It's not meant to be a production-ready SSH replacement ,just my attempt at figuring out how the real thing works.
