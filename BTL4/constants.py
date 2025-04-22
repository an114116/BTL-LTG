import os
import json

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (16, 167, 232)
RED = (206, 10, 10)
GRAY = (107, 99, 99)
DARK_GREY = (41, 41, 46)
ORANGE = (255, 167, 16)
LIGHT_GRAY = (237, 223, 223)
ORANGEDARKER = (200,126,2)

#Utility
WIDTH, HEIGHT = 1200, 650
PATH = ""
FPS = 60
SHIPS = ["Assets/Battleship5.png", "Assets/Submarine3.png", "Assets/RescueShip3.png", "Assets/Cruiser4.png", "Assets/Destroyer2.png"]

#Networking
with open(os.path.join(PATH, "settings/settings.json")) as f:
    settings = json.load(f)
host = settings["serverip"]
port = settings["serverport"]
if not host: host = "127.0.0.1"
if not port: port = 8888
HOST = host
PORT = port

#Networking Messages
"""
1 = When Ships are choosen
"""