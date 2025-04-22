import socket
from _thread import *
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = '0.0.0.0'
port = 6666
server_ip = socket.gethostbyname(server)

try: s.bind((server, port))
except socket.error as e:
    print(f"[ERROR:] {str(e)}")

s.listen()
print("[START:] Waiting for a connection")
connections = []
currentGames = []
lookingForGame = []
currentId = "0"
numConnections = 0
numGames = 0
lookingForGameName = []

def threaded_client(conn):
    global currentId, connections, numConnections, numGames
    data = conn.recv(2048)
    if data:
        currentId = str(len(connections))
        for i in range(len(connections)):
            if connections[i] == None:
                currentId = str(i)
                break
        conn.sendall(str.encode(currentId))
        try: 
            connections[int(currentId)] = conn
        except IndexError:
            connections.append(conn)
        print(f"[INFO:] Number of connections {numConnections}")
    while conn in connections:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if data:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                if len(arr) == 3:
                    arr[2] = int(arr[2])
                    if currentGames[arr[2]][0] == id:
                        connections[currentGames[arr[2]][1]].send(str.encode(arr[1]))
                    elif currentGames[arr[2]][1] == id:
                        connections[currentGames[arr[2]][0]].send(str.encode(arr[1]))
                    if arr[1] == "win":
                        currentGames[arr[2]] = None
                        numGames -= 1
                        print(f"[INFO:] Number of Games {numGames}")
                else:
                    arg = arr[1].split(".")
                    if arg[0] == "lfg":
                        print(f"[INFO:] Adding user {arg[1]} with id {id} to lfg")
                        lookingForGame.append(id)
                        lookingForGameName.append(arg[1])
                if arr[1] == "logout":
                    connections[id] = None
                    numConnections -= 1
                    print(f"[INFO:] Number of connections {numConnections}")
                    if id in lookingForGame:
                        lookingForGame.clear()
                        lookingForGameName.clear()
                    else:
                        try:
                            for i in range(len(currentGames)):
                                if currentGames[i] != None:
                                    if id in currentGames[i]:
                                        currentGames[i] = None
                                        numGames -= 1
                                        print(f"[INFO:] Number of Games {numGames}")
                        except: pass
        except Exception as e:
            print(f"[ERROR:] {e}")
            for i in range(len(connections)):
                if connections[i] == conn:
                    if i in lookingForGame:
                        print("a")
                        lookingForGame.clear()
                        lookingForGameName.clear()
                    try:
                        for x in range(len(currentGames)):
                            if currentGames[x] != None:
                                if i in currentGames[x]:
                                    if i != currentGames[x][0]:
                                        enemy = currentGames[x][0]
                                    else:
                                        enemy = currentGames[x][1]
                                    connections[enemy].send(str.encode("logout"))
                                    currentGames[x] = None
                                    numGames -= 1       
                    except: pass
                    connections[i] = None
                    numConnections -= 1
                    print(f"[INFO:] Number of connections {numConnections}")
                    print(f"[INFO:] Number of Games {numGames}")
            
def threaded_matchGames():
    while True:
        if len(lookingForGame) == 2:
            currentGame = None
            for i in range(len(currentGames)):
                if currentGames[i] == None:
                    currentGame = i
                    break
            if currentGame != None:
                currentGames[currentGame] = [lookingForGame[0], lookingForGame[1]]
                connections[lookingForGame[0]].send(str.encode(f"start:{currentGame}:{lookingForGameName[1]}"))
                connections[lookingForGame[1]].send(str.encode(f"start:{currentGame}:{lookingForGameName[0]}"))
            else:
                currentGames.append([lookingForGame[0], lookingForGame[1]])
                connections[lookingForGame[0]].send(str.encode(f"start:{len(currentGames)-1}:{lookingForGameName[1]}"))
                connections[lookingForGame[1]].send(str.encode(f"start:{len(currentGames)-1}:{lookingForGameName[0]}"))
            global numGames
            numGames += 1
            print(f"[INFO:] Number of Games {numGames}")
            lookingForGame.clear()
            lookingForGameName.clear()

def threaded_Connections():
    while True:
        global numConnections
        conn, addr = s.accept()
        print(f"[INFO:] Connection from: {addr}")
        start_new_thread(threaded_client, (conn,))
        numConnections += 1

lookingForConnectionsThread = threading.Thread(target=threaded_Connections, args=[])
matchGamesThread = threading.Thread(target=threaded_matchGames, args=[])
lookingForConnectionsThread.start()
matchGamesThread.start()
