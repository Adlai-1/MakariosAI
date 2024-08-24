# imports...
import configparser
import socket
import os, sys

sys.path.append(os.path.abspath(os.path.dirname("rag_model")))
from rag_model.model import call_rag

# open config file...
config = configparser.ConfigParser()
config.read("config.ini")

# necessarry variables...
host = str(config['SERVER']['local'])
port = int(config['SERVER']['port'])

# intializing our server...
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port)) 
    
    print("Server up and running!")
    
    server.listen() 

    conn, addr = server.accept()
    print(f"Connection established with {addr}") 
    
    chats = []

    while True:
        data = conn.recv(1024)
        
        if not data: break 
        
        try:
            # Call rag model remotely...
            resp = call_rag(data.decode(), chats)

            for i in range(0, len(resp), 1024):
                conn.send(resp[i:i + 1024].encode())
        except:
            conn.send("Unable to generate a response. Try again later!")