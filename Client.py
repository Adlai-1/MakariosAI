import configparser
import socket
import time
import sys

config = configparser.ConfigParser()
config.read("config.ini")

host = str(config['SERVER']['local'])
port = int(config['SERVER']['port'])

def render_response(message):
    print("Response: ", end="", flush=True)
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.08)  # Adjust this value to change the speed of rendering
    print("\n\n")

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

            # receive
            full_message = ""
            while True:
                chunk = server.recv(2048)
                if not chunk:
                    break
                full_message += chunk.decode()
                if len(chunk) < 2048:
                    break
            
            render_response(full_message)
except:
    print("\nCONNECTION CLOSED!")