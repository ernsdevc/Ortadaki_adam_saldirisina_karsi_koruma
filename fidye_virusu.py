import os
import socket
import getpass
from cryptography.fernet import Fernet

sock = socket.socket()
sock.connect(("10.0.2.4",8080))
sock.send("Merhaba".encode("utf-8"))
sock.close()