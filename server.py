# implementing 3-tier structure: Hall --> Room --> Clients; 
# 14-Jun-2013

import select, socket
from util import Hall, Room, Player

MAX_CLIENTS = 30
HOST = '127.0.0.1'
PORT = 22222
READ_BUFFER = 4096

# create listening sock
def create_sock(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(MAX_CLIENTS)
    return sock

listen_sock = create_sock((HOST, PORT))
listen_sock.setblocking(0)

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    # select.select() will work on both Unix and Windows
    read_sockets, write_socket, error_sockets = select.select(connection_list, [], [])
    for sock in read_sockets:
#        print("connection list:", connection_list)

        if sock is listen_sock: # new connection
            new_socket, add = sock.accept()
            connection_list.append(new_socket)
            new_socket.setblocking(0)
#            print("Registered:", new_socket, new_socket.fileno())
            new_player = Player(new_socket, "new_player")
            player_id, room_id = hall.alloc_room(new_player)
            hall.rooms[room_id].add_player(new_player)

        else: # new message
            msg = sock.recv(READ_BUFFER)
            if msg:
                room_id, player = hall.find_room_player(sock)
                print("msg from room:", room_id, "player:", player)
                hall.rooms[room_id].broadcast(player, msg)
            else:
                sock.close()
                connection_list.remove(sock)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
