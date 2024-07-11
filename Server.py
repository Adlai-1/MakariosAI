# imports...
import configparser
import socket
from RAG_model import saveChat, RAGchain
# open config file...
config = configparser.ConfigParser()
config.read("config.ini")

# necessarry variables...
host = str(config['SERVER']['local'])
port = int(config['SERVER']['port'])

# intializing our server...
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port)) # bind host and port to form a url accessible by clients.
    
    print("Server up and running!") # indicate if server is running
    
    server.listen() # listen-in for client connection requests

    conn, addr = server.accept() # accepts client connection requests
    print(f"Connection established with {addr}") # show client Ip address

    chat_history = [] # storage to hold our conversation history.
    while True:
        data = conn.recv(2048)
        
        if not data: break # very necesssary to not create an infinite loop...
        
        # RAG model magic!
        try:
            response = RAGchain.invoke({'input': data.decode(), 'chat_history': chat_history})

            # Save chat history
            saveChat(data.decode(), response, chat_history)

            # send response in chunks
            for i in range(0, len(response), 2048):
                conn.send(response['answer'][i:i + 2048].encode())
        except:
            conn.send("Unable to generate a response. Try again later!")