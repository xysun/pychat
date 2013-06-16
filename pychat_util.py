# implementing 3-tier structure: Hall --> Room --> Clients; 
# 14-Jun-2013

import socket, pdb

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'


def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return s

class Hall:
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.players = [] # [Player1, player2, ...]
        self.room_player_map = {} # {playerName: roomName}
        self.player_count = 0

    def welcome_new(self, new_socket):
        new_socket.sendall(b'Welcome to pychat.\nPlease tell us your name:\n')

    def list_rooms(self, sock):
        
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            sock.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            sock.sendall(msg.encode())
    
    def handle_msg(self, sock, msg):
        player = self.find_player(sock)
        
        instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch a room\n' \
            + b'[<manual>] to show instructions\n' \
            + b'[<quit>] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

        print(player.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            new_player = Player(sock, name + "@" + str(sock.getsockname()))
            self.players.append(new_player)
            print("New connection from:", new_player.name)
            sock.sendall(instructions)

        elif "<join>" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                room_name = msg.split()[1]
                if player.name in self.room_player_map: # switching?
                    if self.room_player_map[player.name] == room_name:
                        sock.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].players.remove(player)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    self.room_player_map[player.name] = room_name
            else:
                sock.sendall(instructions)

        elif "<list>" in msg:
            self.list_rooms(sock) 

        elif "<manual>" in msg:
            sock.sendall(instructions)
        
        elif "<quit>" in msg:
            sock.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        else:
            # check if in a room or not first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                sock.sendall(msg.encode())
    
    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        self.players.remove(player)
        print("Player: " + player.name + "has left\n")

    
    def find_player(self, player_socket):
        for player in self.players:
            if player.socket == player_socket:
                return player
        return Player(player_socket, "new")

class Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_player):
        msg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(msg.encode())
    
    def broadcast(self, from_player, msg):
        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
            player.socket.sendall(msg)

    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_msg)

class Player:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name
