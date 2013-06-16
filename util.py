# implementing 3-tier structure: Hall --> Room --> Clients; 
# 14-Jun-2013


class Hall:
    def __init__(self):
        self.rooms = [] # [room0, room1, ...]
        self.players = [] # [player1, player2, ...]
        self.room_player_map = {} # {playerID: roomID}
        self.player_count = 0

    def alloc_room(self, new_player): # allocate new player to room; return room ID
        # assuming 2 players for 1 room only
        self.players.append(new_player)
        player_id = len(self.players) - 1
        if self.player_count % 2 == 0: # open a new room 
            self.rooms.append(Room())
        room_id = len(self.rooms) - 1
        self.room_player_map[player_id] = room_id
        self.player_count += 1
        return player_id, room_id

    def remove_player(self, player_socket):
        room_id, player = self.find_room_player(player_socket)
        self.players.remove(player)
        self.rooms[room_id].remove_player(player)
    
    def find_room_player(self, player_socket):
        for player in self.players:
            if player.socket == player_socket:
                room_id = self.room_player_map[self.players.index(player)]
                return room_id, player

class Room:
    def __init__(self):
        self.players = [] # a list of sockets
        pass

    def handle_msg(self, f, from_player): # receive msg from from_player, broadcast f(msg)
        pass

    def broadcast(self, from_player, msg):
        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
            print("player in room: ",player.socket)
            player.socket.sendall(msg)

    def add_player(self, new_player):
        self.players.append(new_player)
        welcome_msg = "Welcome new player: " + new_player.name + '\n'
        self.broadcast(new_player, welcome_msg.encode())

    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = "Player " + player.name + "has left the room"
        self.broadcast(player, leave_msg)

class Player:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name
