import configparser
import socket

# open config file...
config = configparser.ConfigParser()
config.read("config.ini")

# necessarry variables...
host = str(config['SERVER']['local'])
port = int(config['SERVER']['port'])

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port))
        
        while True:
            data = input("Query: ")

            if data.lower() == 'q':
                print("CONNECTION CLOSED!")
                break

            else:
                server.send(data.encode())

            resp = ""
            while True:
                chunk = server.recv(1024)
                if not chunk:
                    break
                resp += chunk.decode()
                if len(chunk) < 1024:
                    break
            
            print(f"Response: {resp}\n")
except:
    print("\nCONNECTION CLOSED!")