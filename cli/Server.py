# imports...
import configparser
import socket
from langserve import RemoteRunnable
import os, sys

sys.path.append(os.path.abspath(os.path.dirname("cli")))

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
    
    while True:
        data = conn.recv(2048)
        
        if not data: break 
        
        try:
            # Call rag model remotely...
            ragChain = RemoteRunnable("http://localhost:8000/ask/")
            input_data = {"input": [{"type": "human", "content": data.decode()}]}
            response = ragChain.invoke(input_data, config={"configurable": {"session_id": "convo"}})

            # send response in chunks
            for i in range(0, len(response), 2048):
                conn.send(response[i:i + 2048].encode())
        except:
            conn.send("Unable to generate a response. Try again later!")