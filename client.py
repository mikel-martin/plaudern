from threading import Thread
import socket

import utils


HOST, PORT = utils.validate_argv()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ask the user for a nickname
name = input("Type username: ")
name = " ".join(name.split()).replace(" ", "-")

# Just when the connection is stablished, 
# the first msg will be the users nickname
client.connect((HOST, PORT))
client.send(name.encode())

# Read the incoming messages and display them
def read():
    while True:
        msg = client.recv(1024)
        msg = msg.decode()
        if msg:
            print(msg)
        else:
            client.close()
            print("Disconnected from the server", 
                "\nType :quit to exit.")
            break

Thread(target=read).start()

# Read whatever msg the user types and send it, 
# unless it is an empty string
while True:
    msg = input()
    if msg != "":
        if msg == ":quit":
            client.send(msg.encode())
            break
        msg = "@" + name + ": " + msg
        client.send(msg.encode())
