import select, socket, sys
from pychat_util import Room, Hall, Player
import pychat_util

READ_BUFFER = 4096

if len(sys.argv) < 2:
    print("Usage: Python3 client.py [hostname]", file = sys.stderr)
    sys.exit(1)
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((sys.argv[1], pychat_util.PORT))

def prompt():
    sys.stdout.write('>')
    sys.stdout.flush()

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, sock]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is sock: # incoming message 
            msg = sock.recv(READ_BUFFER)
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                if msg == pychat_util.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())
                    if 'Please tell us your name' in msg.decode():
                        msg_prefix = 'name: ' # identifier for name
                    else:
                        msg_prefix = ''
                    prompt()

        else:
            msg = msg_prefix + sys.stdin.readline()
            sock.sendall(msg.encode())
