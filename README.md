pychat
======

A Python chat server, with multiple chat rooms, without any frameworks. 

### How to use:
* Download and unzip all the files. You'll also need Python 3 installed. (You can download Python 3 from [here](http://python.org/download/releases/3.3.2/))
* To fire up server: 

"host"(optional) is the ip address your server is running on. It'll default to '', i.e. accepting all connections. 

```python
python3 pychat_server.py [host]
```

* To fire up client: "host"(not optional) should be the same ip address as the server

```python
python3 pychat_client.py host
```

Once running client, you'll see prompts and instructions. 

### Example:
* Text following "$" are command-line inputs
* Text following ">" are user inputs within the client program
* Text following "#" are comments

Server side:

```
$ python3 pychat_server.py 127.0.0.1
Now listening at ('127.0.0.1', 22222)
```

Client1: (create a new chat room "room1")

```
$ python3 pychat_client.py 127.0.0.1
Connected to server

Welcome to pychat.
Please tell us your name:

>joy
Instructions:
[<list>] to list all rooms
[<join> room_name] to join/create/switch to a room
[<manual>] to show instructions
[<quit>] to quit
Otherwise start typing and enjoy!

><list> # list all rooms
Oops, no active rooms currently. Create your own!
Use [<join> room_name] to create a room.

><join> room1
room1 welcomes: joy@('127.0.0.1', 61914)

><list> # list all rooms again
Listing current rooms...
room1: 1 player(s)
```

Client2 (joins room1 that Client1 just created and starts conversation)

```
 # open a new terminal
$ python3 pychat_client.py 127.0.0.1
Connected to server

Welcome to pychat.
Please tell us your name:

>jason
Instructions:
[<list>] to list all rooms
[<join> room_name] to join/create/switch to a room
[<manual>] to show instructions
[<quit>] to quit
Otherwise start typing and enjoy!

><list> # you should see room1 created by Client1
Listing current rooms...
room1: 1 player(s)

><join> room1
room1 welcomes: jason@('127.0.0.1', 61935) # you will also see this message in Client1's window

><list>
Listing current rooms...
room1: 2 player(s)

>hi # Client 1 will also see this, conversation started
jason@('127.0.0.1', 61935):hi

><join> room2 # switch to a new room
room2 welcomes: jason@('127.0.0.1', 61935) # you will see a "leaving message" in Client1's window

><list>
Listing current rooms...
room1: 1 player(s)
room2: 1 player(s)

>hi # Client1 will no longer see this

><quit>
Bye
```

### To do:
* Pass HOST as command-line args [DONE]
* At first connect:
    * Prompt for username [DONE]
    * Prompt instructions [DONE]
* Allow view/select/switch/quit rooms
    * view [DONE]
    * switch [DONE]
* Main server displaying current activities [DONE]
