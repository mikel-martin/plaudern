from threading import Thread
import socket
import sys

import utils


HOST, PORT = utils.validate_argv()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

client_list = []

# Send some kind welcome message to the new client
def welcome_client(conn, name):
    welcome = "#" + name.decode() + " joined the server"
    broadcast(conn, welcome)

# Listen for incoming connections 
# and start a new thread for each one 
def accept_connections():
    while True:
        conn, addr = server.accept()
        Thread(target=client_thread, args=(conn, addr)).start()

# send a message to every connected client.
# the conn parameter is the original sender of the msg
def broadcast(conn, msg):
    print(msg)
    for client in client_list:
        if conn != client["conn"]:
            try:
                client["conn"].send(msg.encode())
            except:
                remove_client(client["conn"])

# read all the incoming messages from a particular client
# and broadcast them to the other users
def client_thread(conn, addr):
    name = conn.recv(1024) # the first msg of the client is his name
    welcome_client(conn, name)
    client_list.append({ "conn": conn, "name": name.decode() }) # keep all the connected clients in a list  
    while True:
        msg = conn.recv(1024)
        msg = msg.decode()
        if msg != "/exit":
            broadcast(conn, msg)
        else:
            remove_client(conn)
            break

# remove a client from the list
def remove_client(name):
    for client in client_list:
        if client["name"] == name: 
            bye = "#" + client["name"] + " left the server."
            broadcast(conn, bye)
            client_list.remove(client)
            conn.close()

# start listening for incoming connections
server.listen() 
print("Server listening on " + HOST + ":" + str(PORT))
accept_connections_thread = Thread(target=accept_connections)
accept_connections_thread.start()
accept_connections_thread.join()
server.close()
