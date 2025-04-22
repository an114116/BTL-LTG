import pygame
from constants import *
import os

#DISPLAY
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load(os.path.join(PATH, r"Assets/logo.png")))

def loadingScreen():
    WIN.fill(BLUE)
    body_font = pygame.font.Font(os.path.join(PATH, "Fonts/INVASION2000.TTF"), 35)
    textName = body_font.render("BattleShip Loading...", 1, ORANGEDARKER)
    loadingTitle = textName.get_rect(center = WIN.get_rect().center)
    WIN.blit(textName, loadingTitle)
    pygame.display.update()

loadingScreen()
pygame.mixer.init()

import socket
from threading import Thread
from string import ascii_uppercase
import sys
from copy import deepcopy
import time
import random
import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter.messagebox import showinfo
import json

def setLanguage(language):
    if not language:
        language = "EN"
    with open(os.path.join(PATH, "languages", language+".json"), "r") as f:
        languageData = json.load(f)
    languageData["titleImage"] = pygame.image.load(os.path.join(PATH, f"Assets/title-{language}.png")).convert_alpha()
    pygame.display.set_caption(languageData["title"])
    return languageData

with open(os.path.join(PATH, "settings/preferences.json"), "r") as f:
    settings = json.load(f)
languageData = setLanguage(settings["language"])

#TITLES
title_font_50 = pygame.font.Font(os.path.join(PATH, "Fonts/INVASION2000.TTF"), 50)
gridFont = pygame.font.Font(os.path.join(PATH, "Fonts/INVASION2000.TTF"), 35)
instruction_font = pygame.font.SysFont(None, 42)
NumbersGridFont = pygame.font.SysFont(None, 45)
body_font = pygame.font.Font(os.path.join(PATH, "Fonts/INVASION2000.TTF"), 35)
smallSettingTexts_font = pygame.font.Font(os.path.join(PATH, "Fonts/INVASION2000.TTF"), 20)

#IMAGES/BUTTONS
rotateButton = pygame.image.load(os.path.join(PATH, r"Assets/Done_button.png")).convert_alpha()
hitImage = pygame.image.load(os.path.join(PATH, r"Assets/hit.png")).convert_alpha()
missImage = pygame.image.load(os.path.join(PATH, r"Assets/miss.png")).convert_alpha()
backgroundImage = pygame.image.load(os.path.join(PATH, r"Assets/Background2.png")).convert_alpha()
logoButton = pygame.image.load(os.path.join(PATH, r"Assets/Logo.png")).convert_alpha()
logoButtonBig = pygame.image.load(os.path.join(PATH, r"Assets/LogoBattleShipBig.png")).convert_alpha()
logoButtonSmall = pygame.image.load(os.path.join(PATH, r"Assets/LogoBattleShipSmall.png")).convert_alpha()
editButton = pygame.image.load(os.path.join(PATH, r"Assets/editicon.png")).convert_alpha()
SettingsButton = pygame.image.load(os.path.join(PATH, r"Assets/SettingsIcon.png")).convert_alpha()
CloseButton = pygame.image.load(os.path.join(PATH, r"Assets/closeIcon.png")).convert_alpha()
MouseClickImage = pygame.image.load(os.path.join(PATH, r"Assets/mouseClicking.png")).convert_alpha()
MouseMiddleClickImage = pygame.image.load(os.path.join(PATH, r"Assets/MiddleClickMouse.png")).convert_alpha()
ArrowKeysImage = pygame.image.load(os.path.join(PATH, r"Assets/ArrowKeys.png")).convert_alpha()
Ship4ConfigMenuImage = pygame.image.load(os.path.join(PATH, r"Assets/Cruiser4.png")).convert_alpha()
Ship2ConfigMenuImage = pygame.image.load(os.path.join(PATH, r"Assets/Destroyer2.png")).convert_alpha()

music = pygame.mixer.Sound(os.path.join(PATH, r"Sounds/valkyries.mp3"))
booms = [pygame.mixer.Sound(os.path.join(PATH, r"Sounds/boom1.mp3")), pygame.mixer.Sound(os.path.join(PATH, r"Sounds/boom2.mp3")), pygame.mixer.Sound(os.path.join(PATH, r"Sounds/boom3.mp3"))]
sink = pygame.mixer.Sound(os.path.join(PATH, r"Sounds/sink.mp3"))
splashes = [pygame.mixer.Sound(os.path.join(PATH, r"Sounds/splash1.mp3")), pygame.mixer.Sound(os.path.join(PATH, r"Sounds/splash2.mp3")), pygame.mixer.Sound(os.path.join(PATH, r"Sounds/splash3.mp3"))]
sounds = [booms, splashes]
pygame.mixer.set_num_channels(20)
music.set_volume(0)
pygame.mixer.find_channel(True).play(music, -1)


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.imageTransformed = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = image
        self.x = x-width/2
        self.y = y
        self.scale = scale
        self.rect = self.imageTransformed.get_rect()
        self.rect.topleft = (self.x,self.y)
    def draw(self):
        try:
            global ShipsList, shipsTouched
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    ShipsList = checkShip()
                    shipsTouched = deepcopy(ShipsList)
                    if ShipsList != False:
                        global shipsDoneMe
                        sendMessage(1)
                        shipsDoneMe = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
        except:
            print("Exeption")
            self.clicked = False
        WIN.blit(self.imageTransformed, (self.rect.x, self.rect.y)) 
    
    def draw2(self):
        try:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and not NotOnWindow:
                self.NewScale = 1
                WIN.blit(logoButtonBig, (self.rect.x - 64/2, self.rect.y - 64/2)) 
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    global menu
                    menu = False
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            else:
                WIN.blit(logoButtonSmall, (self.rect.x, self.rect.y)) 
        except:
            print("Exeption")
            self.clicked = False
    def draw3(self):
        try:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    if ChangeName:
                        InputNamePopUp()
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
        except Exception as e:
            print(e)
            self.clicked = False
        WIN.blit(self.imageTransformed, (self.rect.x, self.rect.y)) 
    
    def draw4(self):
        try:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos) and not NotOnWindow:
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    global settingMenu
                    if settingMenu:
                        settingMenu = False
                    elif not settingMenu:
                        settingMenu = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            WIN.blit(self.imageTransformed, (self.rect.x, self.rect.y)) 
        except:
            print("Exeption")
            self.clicked = False

class Ships:
    def __init__(self, image):
        rect = (0,0,image.get_width(),image.get_height())
        self.rect = pygame.Rect(rect)
        self.click = False
        self.image = image
        self.vertical = False

    def update(self,surface):
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
        surface.blit(self.image,self.rect)
    def move(self):
        pos =  pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False
    
    def rotate(self):
        def turn(self):
            if self.rotated == False:
                self.rotated = True
                if self.vertical == False:
                    self.image = pygame.transform.rotate(self.image, 90)
                    self.vertical = True
                else:
                    self.image = pygame.transform.rotate(self.image, 270)
                    self.vertical = False
                self.rect = self.image.get_rect()
                self.rect.centerx = self.rect.center[0]
                self.rect.centery = self.rect.center[1]
        if self.click:
            keys = pygame.key.get_pressed()
            if self.click == True:
                if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or pygame.mouse.get_pressed()[1] == 1:
                    turn(self)
                else:
                    self.rotated = False

class Slider:
    def __init__(self, display:str, fillColor:tuple, backgroundColor:tuple, outlineColor:tuple, position:int,startedWidth:int = 0):
        self.position = position[0], position[1]
        self.outlineSize = position[2], position[3]
        self.upperValue = 100
        self.display = display
        self.fillColor = fillColor
        self.backgroundColor = backgroundColor
        self.outlineColor = outlineColor
        self.sliderWidth = self.outlineSize[0] * startedWidth // self.upperValue
        self.pressed = False
    def value(self):
        return self.sliderWidth // (self.outlineSize[0] // self.upperValue)
    def draw(self):
        if self.outlineSize[0] - self.sliderWidth == 5: self.finalradius = 4
        elif self.outlineSize[0] - self.sliderWidth == 4: self.finalradius = 5
        elif self.outlineSize[0] - self.sliderWidth == 3: self.finalradius = 6
        elif self.outlineSize[0] - self.sliderWidth == 2: self.finalradius = 7
        elif self.outlineSize[0] - self.sliderWidth <= 1: self.finalradius = 8
        else: self.finalradius = 0
        if self.sliderWidth <= 3: self.initialHeight, self.positionFix = self.outlineSize[1] - 6, self.position[1]+3
        else: self.initialHeight, self.positionFix = self.outlineSize[1], self.position[1]
        pygame.draw.rect(self.display, self.fillColor, (self.position[0], self.position[1], self.outlineSize[0], self.outlineSize[1]), 0, 8)
        pygame.draw.rect(self.display, self.backgroundColor, (self.position[0],self.positionFix, self.sliderWidth, self.initialHeight), 0, self.finalradius,8,self.finalradius,8)
        pygame.draw.rect(self.display, self.outlineColor, (self.position[0]-2, self.position[1]-2, self.outlineSize[0]+4, self.outlineSize[1]+4), 2, 10, -1)
        text = body_font.render(f"{self.value()}%", 1, self.fillColor)
        WIN.blit(text, (self.position[0] + self.outlineSize[0] + 8, self.position[1] - self.outlineSize[1]+7))
    def changeValue(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > self.position[0] and mousePos[0] < self.position[0]  + self.outlineSize[0]:
            if mousePos[1] > self.position[1] and mousePos[1] < self.position[1] + self.outlineSize[1]:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.pressed = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False
        if self.pressed:
            self.sliderWidth = mousePos[0] - self.position[0]
            if self.sliderWidth < 1:
                self.sliderWidth = 0
            if self.sliderWidth > self.outlineSize[0]:
                self.sliderWidth = self.outlineSize[0]

class DropDown:
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.clicked = False 
    def draw(self, surf):
        pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))
        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))
    def update(self):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos) 
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break
        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                return self.active_option
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return -1
    
def InputNamePopUp():
    global root
    root = tk.Tk()
    root.geometry("250x110")
    root.resizable(False, False)
    root.title('Name Input')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (250/2))
    y_cordinate = int((screen_height/2) - (110/2))
    root.geometry("{}x{}+{}+{}".format(250, 110, x_cordinate, y_cordinate))
    photo = PhotoImage(file = os.path.join(PATH, r"Assets/Logo.png"))
    root.iconphoto(False, photo)
    name = tk.StringVar()
    root.attributes('-topmost', True)
    root.update()
    def closing():
        root.destroy()
    def checkKey(event):
        if event.keysym=='Return':
            input()
    def input():
        if not name.get(): showinfo(title='Information', message="Please enter a name!")
        else:
            import re
            if(bool(re.match('^[a-zA-Z0-9]*$', name.get()))==True):
                if len(name.get()) <= 15:
                    if len(name.get()) >= 3:
                        with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
                            data = json.load(f)
                            data["name"] = name.get()
                            f.seek(0)
                            json.dump(data, f, indent=4)
                            f.truncate()
                        closing()
                    else: showinfo(title='Information', message="Name can not be shorter than 3 characters!")
                else: showinfo(title='Information', message="Name can not be longer than 15 characters!")
            else: showinfo(title='Information', message="Please use valid characters!")
    signin = ttk.Frame(root)
    signin.pack(padx=10, pady=10, fill='x', expand=True)
    label = ttk.Label(signin, text="Name:")
    label.pack(fill='x', expand=True)
    entry = ttk.Entry(signin, textvariable=name)
    entry.pack(fill='x', expand=True)
    entry.focus()
    button = ttk.Button(signin, text="Save", command=input)
    button.pack(fill='x', expand=True, pady=10)
    root.bind('<KeyPress>', checkKey)
    root.protocol("WM_DELETE_WINDOW", closing)
    root.mainloop()

def WindowChanger():
    root = tk.Tk()
    root.resizable(False, False)
    root.title('IP Changer')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (250/2))
    y_cordinate = int((screen_height/2) - (110/2))
    root.geometry("{}x{}+{}+{}".format(250, 150, x_cordinate, y_cordinate))
    photo = PhotoImage(file = os.path.join(PATH, r"Assets/Logo.png"))
    root.iconphoto(False, photo)
    ip = tk.StringVar()
    port_var = tk.StringVar()
    root.attributes('-topmost', True)
    root.update()
    def closing():
        root.destroy()
    def checkKey(event):
        if event.keysym=='Return':
            input()
    def input():
        new_ip = ip.get()
        new_port = port_var.get() if port_var.get().isnumeric() else ""
        with open(os.path.join(PATH, "settings/settings.json"), "r+") as f:
            data = json.load(f)
            if new_ip:
                data["serverip"] = new_ip
            if new_port:
                data["serverport"] = int(new_port)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        closing()
    signin = ttk.Frame(root)
    signin.pack(padx=10, pady=10, fill='x', expand=True)
    with open(os.path.join(PATH, 'settings/settings.json')) as f:
        data = json.load(f)
        host = data["serverip"]
        port = data["serverport"]
    if host == '': host = "127.0.0.1"
    label = ttk.Label(signin, text=f"Old IP: {host}")
    label.pack(fill='x', expand=True)
    entry = ttk.Entry(signin, textvariable=ip)
    entry.pack(fill='x', expand=True)
    entry.focus()
    labelPort = ttk.Label(signin, text=f"Old Port: {port}")
    labelPort.pack(fill='x', expand=True)
    entry = ttk.Entry(signin, textvariable=port_var)
    entry.pack(fill='x', expand=True)
    button = ttk.Button(signin, text="Save", command=input)
    button.pack(fill='x', expand=True, pady=10)
    root.bind('<KeyPress>', checkKey)
    root.protocol("WM_DELETE_WINDOW", closing)
    root.mainloop()

def KillEverything():
    pygame.quit()
    if connected: sendMessage(f"logout")
    if gameNum != None: addLoss()
    sys.exit()

def firstConnection():
    while WorkingThreads:
        try:
            global ID, s
            with open(os.path.join(PATH, "settings/settings.json"), "r") as f:
                data = json.load(f)
            HOST = data["serverip"]
            PORT = data["serverport"]
            if HOST == "":
                HOST = "127.0.0.1"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Connecting to server, ' + HOST + ' (' + str(PORT) + ')')
            s.connect((HOST, PORT))
            s.sendall(str.encode("ID Required"))
            data = s.recv(2048)
            if data:
                ID = data.decode('utf-8')
            else:
                raise
            print(f"UserID {ID}")
            t1 = Thread(target=recieveMessage)
            t1.daemon = True
            t1.start()
        except ConnectionRefusedError as e:
            print(e)
            print("Retrying to connect to the server!")
            firstConnection()
        except Exception as e:
            print(e)
            firstConnection()
        finally:
            global connected
            connected = True
            break

def defineOnce(connect):
    WIN.fill(BLACK)
    #Globaling everthing
    global ShipsObjects, rotate_button, LastNumShipMoving, shipsDoneYou, shipsDoneMe, secondConnection, message, startPhase, connected, gameNum, myturn, WorkingThreads, attackCords, saveGuess, saveMyGuess, logo_Button, menu, edit_Button, settings_Button, settingMenu, close_Button, sliders, lastnum, dropDownLanguages, NotOnWindow, NameThreadRunning, ChangeName
    #Define Variable Once
    gameNum = None
    LastNumShipMoving = 0
    shipsDoneYou = False 
    shipsDoneMe = False
    secondConnection = False
    message = None
    startPhase = 0
    myturn = False
    attackCords = None
    saveGuess = []
    menu = True
    settingMenu = False
    lastnum = 0
    NotOnWindow = False
    NameThreadRunning = False
    ChangeName = True
    #Create Ships Objects
    ShipsObjects = []
    saveMyGuess = []
    for i in range(len(SHIPS)):
        ShipsObjects.append(Ships(pygame.image.load(os.path.join(PATH, f"{SHIPS[i]}")).convert_alpha()))
        ShipsObjects[i].rect.center = (WIDTH // 2, 135 + 35*i)
    #Define Button
    rotate_button = Button(600, 400, rotateButton, 1)
    logo_Button = Button(WIDTH//2, HEIGHT//2-150, logoButtonSmall, 1)
    edit_Button = Button(WIDTH//2, 115, editButton, 1)
    settings_Button = Button(WIDTH-30, HEIGHT-45, SettingsButton, 1)
    close_Button = Button(WIDTH-60, 45, CloseButton, 1)
    with open(os.path.join(PATH, 'settings/preferences.json')) as f:
        volumes = json.load(f)["volume"]
    volumes = volumes.split(",")
    if len(volumes) != 2:
        with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
            data = json.load(f)
            data["volume"] = "50,50"
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        volumes = data["volume"].split(",")
    sliders = [Slider(WIN, (255, 255, 255), (177, 177, 177), (0, 0, 0), (100, 150, 400, 20), int(volumes[0])), Slider(WIN, (255, 255, 255), (177, 177, 177), (0, 0, 0), (100, 200, 400, 20), int(volumes[1]))]
    with open(os.path.join(PATH, 'settings/preferences.json')) as f:
        language = json.load(f)["language"]
    if language == "": language = "English"
    elif language == "EN": language = "English"
    elif language == "ES": language = "Spanish (Español)"
    dropDownLanguages = DropDown([ORANGEDARKER, ORANGEDARKER],[(177, 177, 177), GRAY], 100, 300, 400, 50, pygame.font.SysFont(None, 30), language, ["English", "Spanish (Español)"])
    #Start Networking
    if connect:
        WorkingThreads = True
        connected = False
        connThread = Thread(target=firstConnection)
        connThread.daemon = True
        connThread.start() 

def draw_background():
    WIN.fill(GRAY)
    pygame.draw.line(WIN, DARK_GREY, (10, 10), (1190, 10))
    pygame.draw.line(WIN, DARK_GREY, (1190, 10), (1190, 630))
    pygame.draw.line(WIN, DARK_GREY, (1190, 560), (10, 560))
    pygame.draw.line(WIN, DARK_GREY, (10, 10), (10, 630))
    pygame.draw.line(WIN, DARK_GREY, (10, 630), (1190, 630))

def draw_titles():
    title_text = title_font_50.render(languageData["titlewin"], True, BLACK, None)
    title_text_rect = title_text.get_rect(center=(WIN.get_rect().centerx, 38))
    player_text = gridFont.render(languageData["gridplayer"], True, BLACK, None)
    player_text_rect = player_text.get_rect(center=(212+75, 90))
    enemy_text = gridFont.render(f"{OPONENTNAME}{languageData['gridenemy']}", True, BLACK, None)
    enemy_text_rect = enemy_text.get_rect(center=(920,90))
    WIN.blit(title_text, title_text_rect)
    WIN.blit(player_text, player_text_rect)
    WIN.blit(enemy_text, enemy_text_rect)

def draw_grid():
    pygame.draw.rect(WIN, BLUE, pygame.Rect(75 + 17, 120, 495-75 -35,520-135))
    pygame.draw.rect(WIN, ORANGE, pygame.Rect(75 + 17, 120, 495-75 -35,35))
    pygame.draw.rect(WIN, ORANGE, pygame.Rect(75 + 17, 120, 35,520-135))

    pygame.draw.rect(WIN, BLUE, pygame.Rect(WIDTH - 497 + 17, 120, 420-35,520-135))
    pygame.draw.rect(WIN, ORANGE, pygame.Rect(WIDTH - 497 + 17, 120, 420-35, 35))
    pygame.draw.rect(WIN, ORANGE, pygame.Rect(WIDTH - 497 + 17, 120, 35, 520-135))
    grid_x = 75 + 17
    grid_y = 120
    for _ in range(12):
        pygame.draw.line(WIN, BLACK, (grid_x, 120), (grid_x, 542-35), 4)
        pygame.draw.line(WIN, BLACK, (75 + 17, grid_y), (497-35  + 17, grid_y), 4)
        grid_x += 35 
        grid_y += 35
    grid_x = WIDTH - 497 + 17 
    grid_y = 120
    for _ in range(12):
        pygame.draw.line(WIN, BLACK, (grid_x, 120), (grid_x, 542-35), 4)
        pygame.draw.line(WIN, BLACK, (WIDTH - 497 + 17, grid_y), (WIDTH - 75 -35 + 17, grid_y), 4)
        grid_x += 35
        grid_y += 35
    widthListNumbers = [9, 8, 9, 9, 8, 9, 9, 9, 9, 9]
    widthListLetters = [0, 0, 0, 0, 0, 1, 0, 0, 7, 3]
    heightListNumbers = [0, -1, 0, 0, -1, 0, 0, 0, 1.5, -1]
    for x in range(10):
        img = NumbersGridFont.render(f'{x}', True, LIGHT_GRAY)
        WIN.blit(img, ((x+1)*35 + 111 - widthListNumbers[x], 116 + heightListNumbers[x] + 18/2))
        img = NumbersGridFont.render(f'{ascii_uppercase[x]}', True, LIGHT_GRAY)
        WIN.blit(img, (99 + widthListLetters[x], (x+1)*35 + 116 + 9))
    for x in range(10):
        img = NumbersGridFont.render(f'{x}', True, LIGHT_GRAY)
        WIN.blit(img, ((x+1)*35 + 739 - widthListNumbers[x], 116 + heightListNumbers[x] + 18/2))
        img = NumbersGridFont.render(f'{ascii_uppercase[x]}', True, LIGHT_GRAY)
        WIN.blit(img, (728 + widthListLetters[x], (x+1)*35 + 116 + 9))

def draw_buttons():
    rotate_button.draw()

def draw_ships(ShipsObjects):
    for i in range(len(ShipsObjects)):
        ShipsObjects[i].update(WIN)

def moveShips(ShipsObjects):
    for i in range(len(ShipsObjects)):
        global LastNumShipMoving
        if not ShipsObjects[LastNumShipMoving].click:
            LastNumShipMoving = i
            ShipsObjects[LastNumShipMoving].move()
            ShipsObjects[LastNumShipMoving].rotate()
        else:
            ShipsObjects[LastNumShipMoving].move()
            ShipsObjects[LastNumShipMoving].rotate()

def checkShip():
    ShipList = []
    num = 0
    for i in range(len(ShipsObjects)):
        if not ShipsObjects[i].vertical:
            x, y, length = round((ShipsObjects[i].rect[0] - 128)/35), round((ShipsObjects[i].rect[1] - 174 + round(ShipsObjects[i].rect[3]/2))/35), round(ShipsObjects[i].rect[2]/35)
            vertical = False
        else:
            x, y, length = round(((ShipsObjects[i].rect[0] - 150) + round(ShipsObjects[i].rect[2]/2))/35), round((ShipsObjects[i].rect[1] - 156)/35), round(ShipsObjects[i].rect[3]/35)
            vertical = True
        if y >= 0 and y <=10 and x >= 0 and x <=10:
            if vertical:
                if y + length <= 10:
                    ShipList.append([])
                    for a in range(length):
                        ShipList[num].append((x,y+a))
                    num += 1
            else:
                if x + length <= 10:
                    ShipList.append([])
                    for a in range(length):
                        ShipList[num].append((x+a,y))
                    num += 1
    repeated = False
    AllShips = False
    waterGapLeft = True
    if len(ShipList) == len(ShipsObjects):
        AllShips = True
  
    ShipListTogether = []
    for i in range(len(ShipList)):
        for x in range(len(ShipList[i])):  
            ShipListTogether.append(ShipList[i][x])
    for i in range(len(ShipListTogether)):
        for x in range(len(ShipListTogether)):
            if ShipListTogether[i] == ShipListTogether[x]:
                if i != x:
                    repeated = True
                    break
    global AroundShip
    AroundShip = []
    for i in range(len(ShipList)):
        AroundShip.append([])
        if not ShipsObjects[i].vertical:
            for x in range(len(ShipList[i])):
                AroundShip[i].append(((ShipList[i][x][0], ShipList[i][x][1]+1)))
                AroundShip[i].append(((ShipList[i][x][0], ShipList[i][x][1]-1)))
            AroundShip[i].append((ShipList[i][0][0]-1, ShipList[i][0][1]))
            AroundShip[i].append((ShipList[i][0][0]-1, ShipList[i][0][1]-1))
            AroundShip[i].append((ShipList[i][0][0]-1, ShipList[i][0][1]+1))
            AroundShip[i].append((ShipList[i][len(ShipList[i])-1][0]+1, ShipList[i][0][1]))
            AroundShip[i].append((ShipList[i][len(ShipList[i])-1][0]+1, ShipList[i][0][1]-1))
            AroundShip[i].append((ShipList[i][len(ShipList[i])-1][0]+1, ShipList[i][0][1]+1))
        if ShipsObjects[i].vertical:
            for x in range(len(ShipList[i])):
                AroundShip[i].append(((ShipList[i][x][0]+1, ShipList[i][x][1])))
                AroundShip[i].append(((ShipList[i][x][0]-1, ShipList[i][x][1])))
            AroundShip[i].append((ShipList[i][0][0], ShipList[i][0][1]-1))
            AroundShip[i].append((ShipList[i][0][0]-1, ShipList[i][0][1]-1))
            AroundShip[i].append((ShipList[i][0][0]+1, ShipList[i][0][1]-1))
            AroundShip[i].append((ShipList[i][len(ShipList[i])-1][0], ShipList[i][len(ShipList[i])-1][1]+1))
            AroundShip[i].append((ShipList[i][len(ShipList[i])-1][0]+1, ShipList[i][len(ShipList[i])-1][1]+1))
            AroundShip[i].append((ShipList[i][len(ShipList[i])-1][0]-1, ShipList[i][len(ShipList[i])-1][1]+1))
    AroundShipListTogether = []
    for i in range(len(AroundShip)):
        for x in range(len(AroundShip[i])):  
            AroundShipListTogether.append(AroundShip[i][x])
    for i in range(len(AroundShipListTogether)):
        for x in range(len(ShipListTogether)):
            if AroundShipListTogether[i] == ShipListTogether[x]:
                if i != x:
                    waterGapLeft = False
                    break
    global message
    if not AllShips:
        message = languageData["downmessageerrorships1"]
        return False
    elif repeated:
        message =  languageData["downmessageerrorships2"]
        return False
    elif not waterGapLeft:
        message =  languageData["downmessageerrorships3"]
        return False
    else:
        for i in range(len(ShipList)):
            if not ShipsObjects[i].vertical:
                ShipsObjects[i].rect[1] = (ShipList[i][0][1])*35 + 173 - round(ShipsObjects[i].rect[3]/2)
                ShipsObjects[i].rect[0] = (ShipList[i][0][0])*35 + 128 
                ShipsObjects[i].update(WIN)
            else:
                ShipsObjects[i].rect[1] = (ShipList[i][0][1])*35 + 154
                ShipsObjects[i].rect[0] = (ShipList[i][0][0])*35 + 145 - round(ShipsObjects[i].rect[2]/2)
                ShipsObjects[i].update(WIN)
    return ShipList

def updateMessage(Message):
    pygame.draw.rect(WIN, GRAY, pygame.Rect(10, 520, 1190, 560))
    pygame.draw.line(WIN, DARK_GREY, (1190, 560), (10, 560))
    pygame.draw.line(WIN, DARK_GREY, (10, 10), (10, 630))
    pygame.draw.line(WIN, DARK_GREY, (10, 630), (1190, 630))
    pygame.draw.line(WIN, DARK_GREY, (1190, 10), (1190, 630))
    text = instruction_font.render(Message, True, WHITE)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, 590)
    WIN.blit(text, textRect)

def recieveMessage():
    global secondConnection, shipsDoneYou, gameNum, attackCords, OPONENTNAME
    try:
        while WorkingThreads:
            data = s.recv(2048)
            reply = data.decode('utf-8')
            if not reply:
                raise ConnectionResetError
            if ":" in reply:
                arr = reply.split(":")
                if arr[0] == "start":
                    secondConnection = True
                    gameNum = arr[1]
                    OPONENTNAME = arr[2]
            elif "." in reply:
                answ = reply.split(".")
                if answ[0] == "attack":
                    attackCords = answ[1]
                elif answ[0] == "guessAnswer":
                    touchedShip = answ[1]
                    x = answ[2]
                    y = answ[3]
                    addGuess(touchedShip, int(x), int(y))
            if reply == "1":
                shipsDoneYou = True
            if reply == "logout":
                displayMessageMenu(languageData["winbyleft"])
                addWin()
                defineOnce(False)
            if reply == "win":
                displayMessageMenu(languageData["regularwin"])
                addWin()
                defineOnce(False)
    except ConnectionResetError as e:
        print(e)
        displayMessageMenu(languageData["serverdownmidgame"])
        defineOnce(True)

def sendMessage(message):
    global gameNum
    if gameNum == None: request = f"{ID}:{message}" 
    else: request = f"{ID}:{message}:{gameNum}" 
    s.sendall(str.encode(request))

def checkTurn():
    global attackCords, myturn
    if myturn == True:
        updateMessage(languageData["yourturn"])
        if pygame.mouse.get_pressed()[0] == 1:
            pos = pygame.mouse.get_pos()
            x,y = (pos[0]-757)//35, (pos[1]-157)//35
            if x >= 0 and y >= 0 and x <= 9 and y <= 9:
                alreadyGuessed = False
                for i in range(len(saveGuess)):
                    if str(x *35 + 757) in str(saveGuess[i][1]) and str(y * 35 + 157) in str(saveGuess[i][2]):
                        alreadyGuessed = True
                if not alreadyGuessed:
                    sendMessage(f"attack.{(x,y)}")
                    myturn = False
    elif not myturn and attackCords != None:
        cords = attackCords
        attackCords = None
        myturn = True
        return cords
    elif not myturn:
        updateMessage(f'{languageData["notyourturn1"]} {OPONENTNAME} {languageData["notyourturn2"]}')

def checkCords(cords):
    global shipsTouched, saveMyGuess
    touchedShip = False
    for i in range(len(ShipsList)):
        for x in range(len(ShipsList[i])):
            if str(ShipsList[i][x]) == cords:
                touchedShip = True
                lasti = i
                lastx = x
                break
    splited = cords.split(",")
    splited[0] = splited[0][1:]
    splited[1] = splited[1][:-1]
    cordinatesList = [int(splited[0]),int(splited[1])]
    entireShip = False
    if touchedShip:
        cordinatesFound = [lasti,lastx]
        shipsTouched[cordinatesFound[0]][cordinatesFound[1]] = None
        entireShip = True
        for i in range(len(shipsTouched[cordinatesFound[0]])):
            if shipsTouched[cordinatesFound[0]][i] != None:
                entireShip = False
        sendMessage(f"guessAnswer.{touchedShip}.{cordinatesList[0]*35 + 757}.{cordinatesList[1]* 35 + 157}")
        saveMyGuess.append([hitImage, cordinatesList[0]*35 + 129, cordinatesList[1]* 35 + 157])
    else:
        sendMessage(f"guessAnswer.{False}.{cordinatesList[0]*35 + 757}.{cordinatesList[1]* 35 + 157}")
        saveMyGuess.append([missImage, cordinatesList[0]*35 + 129, cordinatesList[1]* 35 + 157])
    if entireShip:
        for u in range(len(AroundShip[cordinatesFound[0]])):
            if not 10 in AroundShip[cordinatesFound[0]][u] and not -1 in AroundShip[cordinatesFound[0]][u]:
                sendMessage(f"guessAnswer.{False}.{AroundShip[cordinatesFound[0]][u][0]*35 + 757}.{AroundShip[cordinatesFound[0]][u][1]* 35 + 157}")
                saveMyGuess.append([missImage, AroundShip[cordinatesFound[0]][u][0]*35 + 129, AroundShip[cordinatesFound[0]][u][1] * 35 + 157])
                time.sleep(0.08)
    finished = True
    for i in range(len(shipsTouched)):
        for x in range(len(shipsTouched[i])):
            if shipsTouched[i][x] != None:
                finished = False
    if finished:
        sendMessage("win")
        addLoss()
        displayMessageMenu("You Lost!")
        defineOnce(False)

def addGuess(touchedShip, x, y):
    global saveGuess
    if touchedShip == "True": 
        image = hitImage
        randomBoomSound = random.choice(booms)
        pygame.mixer.find_channel(True).play(randomBoomSound)
    else: 
        image = missImage
        randomWaterSound = random.choice(splashes)
        pygame.mixer.find_channel(True).play(randomWaterSound)
    saveGuess.append([image, x, y])

def drawGuesses():
    global saveGuess, saveMyGuess
    for i in range(len(saveGuess)):
        WIN.blit(saveGuess[i][0], (saveGuess[i][1], saveGuess[i][2]))
    for i in range(len(saveMyGuess)):
        WIN.blit(saveMyGuess[i][0], (saveMyGuess[i][1], saveMyGuess[i][2]))

def addWin():
    with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
        data = json.load(f)
        if data["wins"] == "":
            data["wins"] = 0
        data["wins"] = int(data["wins"])+1
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def addLoss():
    with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
        data = json.load(f)
        if data["losses"] == "":
            data["losses"] = 0
        data["losses"] = int(data["losses"])+1
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

# Main Game Functions
def startRunning():
    global startPhase, menu, ChangeName
    if startPhase == 0:
        if connected:
            with open(os.path.join(PATH, 'settings/preferences.json')) as f:
                name = json.load(f)["name"]
            if name == "None" or name == None:
                menu = True
                displayMessageMenu(languageData["namerequired"])
            else:
                sendMessage(f"lfg.{name}") #Looking for game
                ChangeName = False
                startPhase = 1   
        else: 
            menu = True
            displayMessageMenu(languageData["connectservererror"])
    else:
        if not settingMenu:
            mainMenu() 
        body_font.set_underline(True)
        textError = body_font.render("Waiting for second player...", 1, RED)
        width = textError.get_width()
        WIN.blit(textError, (WIDTH//2-width//2, 400))
        body_font.set_underline(False)

def waitingBoats():
    draw_background()
    draw_titles()
    draw_grid()
    draw_ships(ShipsObjects)
    updateMessage(languageData["downmessage1"])
    global myturn
    myturn = True

def chooseBoats():
    global startPhase, settingMenu
    if startPhase == 1:
        settingMenu = False
        startPhase = 2
    draw_background()
    draw_titles()
    draw_grid()
    draw_buttons()
    moveShips(ShipsObjects)
    updateMessage(languageData["downmessage2"])
    draw_ships(ShipsObjects)
    global message
    if message != None:
        updateMessage(message)

def gameStart():
    draw_background()
    draw_grid()
    draw_titles()
    draw_ships(ShipsObjects)
    cords = checkTurn()
    if not not cords: 
        checkCords(cords)
    drawGuesses()

def mainGame():
    Phase = 0
    if secondConnection: Phase = 1
    if shipsDoneMe: Phase = 2
    if shipsDoneYou and shipsDoneMe: Phase = 3
    
    if Phase == 0: startRunning()
    elif Phase == 1: chooseBoats()
    elif Phase == 2: waitingBoats()
    elif Phase == 3: gameStart()

def displayMessageMenu(message=None):
    global start_ticks, displayMessage
    try:
        if message != None:
            displayMessage = message
            start_ticks=pygame.time.get_ticks()
    except:pass
    try:
        seconds=(pygame.time.get_ticks()-start_ticks)//1000
        if seconds <= 3:
            body_font.set_underline(True)
            textError = body_font.render(displayMessage, 1, RED)
            width = textError.get_width()
            WIN.blit(textError, (WIDTH//2-width//2, 400))
            body_font.set_underline(False)
    except:pass

def mainMenu():
    if not settingMenu:
        WIN.blit(backgroundImage, (0,0))
        title_center = languageData["titleImage"].get_rect(center = WIN.get_rect().center)
        title_center[1] = 20
        WIN.blit(languageData["titleImage"], title_center)
        with open(os.path.join(PATH, 'settings/preferences.json')) as f:
            name = json.load(f)["name"]
        if name == "":
            name = "None"
            with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
                data = json.load(f)
                data["name"] = name
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        textName = body_font.render(name, 1, ORANGEDARKER)
        title_center = textName.get_rect(center = WIN.get_rect().center)
        title_center[1] = 105
        WIN.blit(textName, title_center)
        with open(os.path.join(PATH, 'settings/preferences.json')) as f:
            data = json.load(f)
        wins = data["wins"]
        if not wins: wins = 0
        losses = data["losses"]
        if not losses: losses = 0
        textWin = body_font.render(f'{languageData["wins"]}: {wins}', 1, ORANGEDARKER)
        textLoss = body_font.render(f'{languageData["losses"]}: {losses}', 1, ORANGEDARKER)
        WIN.blit(textWin, (10, 10))
        WIN.blit(textLoss, (10, 40))
        logo_Button.draw2()
        edit_Button.rect.x = title_center[2] + title_center[0] + 3 #for the end
        #edit_Button.rect.x = title_center[0] - 25 #for the beggining
        edit_Button.draw3()
        settings_Button.draw4()

def settingsMenu():
    if settingMenu:
        global lastnum, languageData
        WIN.fill(BLUE)
        close_Button.draw4()
        for i in range(len(sliders)):
            if not sliders[lastnum].pressed:
                lastnum = i
                sliders[lastnum].changeValue()
            else:
                sliders[lastnum].changeValue()
            for i in range(len(sliders)):
                sliders[i].draw()
            volumeText = body_font.render(languageData["volumesettings"], 1, ORANGEDARKER)
            musicVolumeText = smallSettingTexts_font.render(languageData["musicsettings"], 1, ORANGEDARKER)
            soundsVolumeText = smallSettingTexts_font.render(languageData["soundssettings"], 1, ORANGEDARKER)
            WIN.blit(volumeText, (100, 75))
            WIN.blit(musicVolumeText, (100, 125))
            WIN.blit(soundsVolumeText, (100, 175))
            with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
                data = json.load(f)
                data["volume"] = f"{sliders[0].value()},{sliders[1].value()}"
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        languageText = body_font.render(languageData["languagesettings"], 1, ORANGEDARKER)
        WIN.blit(languageText, (100, 250))
        selected_option = dropDownLanguages.update()
        if selected_option >= 0:
            dropDownLanguages.main = dropDownLanguages.options[selected_option]
            if dropDownLanguages.main == "Spanish (Español)":
                language = "ES"
            elif dropDownLanguages.main == "English":
                language = "EN"
            with open(os.path.join(PATH, "settings/preferences.json"), "r+") as f:
                data = json.load(f)
                data["language"] = language
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            languageData = setLanguage(language)
        dropDownLanguages.draw(WIN)
        WIN.blit(soundsVolumeText, (100, 175))

        controlsText = body_font.render(languageData["controlsmenu"], 1, ORANGEDARKER)
        shipsMoveText = smallSettingTexts_font.render(languageData["moveshipsmenu"], 1, ORANGEDARKER)
        MoveShipsExplanationText1 = smallSettingTexts_font.render(languageData["moveshipsmenu"], 1, ORANGEDARKER)
        MoveShipsExplanationText2 = smallSettingTexts_font.render(languageData["moveshipsinstructions2"], 1, ORANGEDARKER)
        WIN.blit(controlsText, (WIDTH-210-321, 75))
        WIN.blit(shipsMoveText, (WIDTH-210-321, 125))
        WIN.blit(Ship4ConfigMenuImage, (WIDTH-210-321+2, 170))
        WIN.blit(MouseClickImage, (WIDTH-210-321+30, 160))
        WIN.blit(MoveShipsExplanationText1, (WIDTH-210-321+120, 160))
        WIN.blit(MoveShipsExplanationText2, (WIDTH-210-321+120, 175))

        shipsMoveText = smallSettingTexts_font.render(languageData["rotateshipsmenu"], 1, ORANGEDARKER)
        MoveShipsExplanationText1 = smallSettingTexts_font.render(languageData["rotateshipsinstructions1"], 1, ORANGEDARKER)
        MoveShipsExplanationText2 = smallSettingTexts_font.render(languageData["rotateshipsinstructions2"], 1, ORANGEDARKER)
        MoveShipsExplanationText3 = smallSettingTexts_font.render(languageData["rotateshipsinstructions3"], 1, ORANGEDARKER)
        MoveShipsExplanationText4 = smallSettingTexts_font.render(languageData["rotateshipsinstructions4"], 1, ORANGEDARKER)
        WIN.blit(shipsMoveText, (WIDTH-210-321, 230))
        ShipConfigMenuRotated = pygame.transform.rotate(Ship2ConfigMenuImage, 90)
        WIN.blit(ShipConfigMenuRotated, (WIDTH-210-321+2, 275))
        MouseClickImageScaled = pygame.transform.scale(MouseClickImage, (int(MouseClickImage.get_width() * 0.7), int(MouseClickImage.get_height() * 0.7)))
        WIN.blit(MouseClickImageScaled, (WIDTH-210-321-3, 290))
        WIN.blit(MouseMiddleClickImage, (WIDTH-210-321+40, 275))
        WIN.blit(ArrowKeysImage, (WIDTH-210-321+50, 320))
        WIN.blit(MoveShipsExplanationText1, (WIDTH-210-321+120, 265+10))
        WIN.blit(MoveShipsExplanationText2, (WIDTH-210-321+120, 280+10))
        WIN.blit(MoveShipsExplanationText3, (WIDTH-210-321+120, 295+10))
        WIN.blit(MoveShipsExplanationText4, (WIDTH-210-321+120, 310+10))
        
    music.set_volume(sliders[0].value()*.01)
    for i in range(len(sounds)):
        for x in range(len(sounds[i])):
            sounds[i][x].set_volume(sliders[1].value())
    sink.set_volume(sliders[1].value())

def main():
    clock = pygame.time.Clock()
    run = True
    defineOnce(True)
    while run:
        clock.tick(FPS)
        global NotOnWindow
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.WINDOWFOCUSLOST:
                NotOnWindow = True
            if event.type == pygame.WINDOWFOCUSGAINED:
                NotOnWindow = False
            if event.type == pygame.KEYUP and event.unicode == "\x1b": #ESCAPE
                global settingMenu
                if not settingMenu: settingMenu = True
                elif settingMenu: settingMenu = False
        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT and mods & pygame.KMOD_ALT and keys[pygame.K_F5] and settingMenu and not superSecretSetting:
            superSecretSetting = True
            WindowChanger()
        else: superSecretSetting = False
        if menu: 
            mainMenu()
            displayMessageMenu()
        elif not menu: mainGame()
        settingsMenu()
        pygame.display.update()
    KillEverything()
    
if __name__ == "__main__":
    main()