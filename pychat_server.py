# implementing 3-tier structure: Hall --> Room --> Clients; 
# 14-Jun-2013

import select, socket, sys, pdb
from pychat_util import Hall, Room, Player
import pychat_util

READ_BUFFER = 4096

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = pychat_util.create_socket((host, pychat_util.PORT))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    read_sockets, write_socket, error_sockets = select.select(connection_list, [], [])
    for sock in read_sockets:
        if sock is listen_sock: # new connection
            new_socket, add = sock.accept()
            connection_list.append(new_socket)
            new_socket.setblocking(0)
            hall.welcome_new(new_socket)

        else: # new message
            msg = sock.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(sock, msg)
            else:
                sock.close()
                connection_list.remove(sock)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
