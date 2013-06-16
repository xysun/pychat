import select, socket, sys
from util import Room, Hall, Player

HOST = '127.0.0.1'
PORT = 22222
READ_BUFFER = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((HOST, PORT))

def prompt():
    sys.stdout.write('<You>\n')
    sys.stdout.flush()

print("Connected to server\n")
prompt()

socket_list = [sys.stdin, sock]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is sock: # incoming message 
            msg = sock.recv(READ_BUFFER)
            if not msg:
                print("msg empty!")
            else:
                sys.stdout.write(msg.decode())
                prompt()

        else:
            msg = sys.stdin.readline()
            sock.sendall(msg.encode())
            prompt()
