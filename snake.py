#!/usr/bin/python
# -*- coding: utf-8 -*-


import random

from tkinter import Tk, Frame, Canvas, ALL, Label, Button, StringVar
from tkinter import colorchooser

import os

DELTA_FOR_BLOCK = 4
WIDTH = 300
HEIGHT = 300
DELAY = 120
ELEMENT_SIZE = 10
ALL_ELEMENTS = WIDTH * HEIGHT / (ELEMENT_SIZE * ELEMENT_SIZE)
RAND_POSITION = 27
tk = Tk()

COUNT_LABEL = StringVar()
BACKGROUND_LABEL = StringVar()
SNAKE_COLOR_LABEL = StringVar()
TARGET_COLOR_LABEL = StringVar()
SPEED_PLUS_LABEL = StringVar()
SPEED_MINUS_LABEL = StringVar()
PAUSE_RESUME_LABEL = StringVar()
NEW_GAME_LABEL = StringVar()
ENG_RUS_LABEL = StringVar()
QUIT_LABEL = StringVar()

COUNT = 0
RATING = 1
PAUSE = False
score_list = []


def updateRatingTable():
    global score_list

    exists = os.path.isfile('rating.txt')
    if exists:
        f = open("rating.txt", "r")
        contents = f.read()

    else:
        contents = ''
    score_list = []
    for score in contents.split("\n"):
        if score != "":
            score_list.append(int(score))
    score_list.append(COUNT)
    # удаляем повторения
    score_list = list(set(score_list))
    score_list.sort(reverse=True)
    if len(score_list) > 9:
        score_list = score_list[:9]
    if exists:
        f.close()
    f = open("rating.txt", "w")
    for score in score_list:
        f.write(str(score) + "\n")
    f.close()


def updateRating():
    global score_list
    global RATING
    cur_rating = 1
    if not score_list:
        RATING = 1
    else:
        for score in score_list:
            if COUNT >= score:
                break
            else:
                cur_rating += 1

    RATING = cur_rating
    tmp_label = str(COUNT) + "/" + str(RATING)
    COUNT_LABEL.set(tmp_label)


updateRatingTable()
updateRating()


class GameBoard(Canvas):
    def __init__(self, master):

        Canvas.__init__(self, master, width=WIDTH, height=HEIGHT)
        self.init()

    def init(self):
        global LANGUAGE

        updateRatingTable()
        updateRating()

        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.gameOn = True
        self.elements = 3

        self.target_x = 100
        self.target_y = 190

        # 0 русский 1 английский
        LANGUAGE = 0
        BACKGROUND_LABEL.set("Цвет фона")
        SNAKE_COLOR_LABEL.set("Цвет змейки")
        TARGET_COLOR_LABEL.set("Цвет цели")
        SPEED_PLUS_LABEL.set("Скорость +")
        SPEED_MINUS_LABEL.set("Скорость -")
        PAUSE_RESUME_LABEL.set("Пауза/возобновить")
        NEW_GAME_LABEL.set("Новая игра")
        ENG_RUS_LABEL.set("Анг/рус")
        QUIT_LABEL.set("Завершить")

        self.focus_get()
        self.createObjects()
        self.locateTarget()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(DELAY, self.onTimer)

    def createObjects(self):
        self.create_rectangle(self.target_x, self.target_y,
                              self.target_x + 4, self.target_y + 4,
                              fill="yellow", tag="target")

        self.create_rectangle(50, 50, 50 + DELTA_FOR_BLOCK,
                              50 + DELTA_FOR_BLOCK, fill="red", tag="head")
        self.create_rectangle(30, 50, 30 + DELTA_FOR_BLOCK,
                              50 + DELTA_FOR_BLOCK, fill="orange",
                              tag="element")
        self.create_rectangle(40, 50, 40 + DELTA_FOR_BLOCK,
                              50 + DELTA_FOR_BLOCK, fill="orange",
                              tag="element")

    def checkTarget(self):
        global COUNT, COUNT_LABEL

        target = self.find_withtag("target")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if target[0] == ovr:
                COUNT += 1
                updateRating()
                tmp_label = str(COUNT) + "/" + str(RATING)
                COUNT_LABEL.set(tmp_label)

                x = self.coords(target)[0]
                y = self.coords(target)[1]
                self.create_rectangle(x, y,
                                      x + DELTA_FOR_BLOCK,
                                      y + DELTA_FOR_BLOCK,
                                      fill="orange", tag="element")
                self.locateTarget()

    def doMove(self):

        elements = self.find_withtag("element")
        head = self.find_withtag("head")

        items = elements + head

        z = 0
        while z < len(items) - 1:
            c1 = self.coords(items[z])
            c2 = self.coords(items[z + 1])
            self.move(items[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1

        if self.left:
            self.move(head, -ELEMENT_SIZE, 0)

        if self.right:
            self.move(head, ELEMENT_SIZE, 0)

        if self.up:
            self.move(head, 0, -ELEMENT_SIZE)

        if self.down:
            self.move(head, 0, ELEMENT_SIZE)

    def checkCollisions(self):

        elements = self.find_withtag("element")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for element in elements:
            for over in overlap:
                if over == element:
                    self.gameOn = False

        if x1 < - ELEMENT_SIZE:
            self.gameOn = False

        if x1 > WIDTH:
            self.gameOn = False

        if y1 < - ELEMENT_SIZE:
            self.gameOn = False

        if y1 > HEIGHT:
            self.gameOn = False

    def locateTarget(self):

        target = self.find_withtag("target")
        self.delete(target[0])

        r = random.randint(0, RAND_POSITION)
        self.target_x = r * ELEMENT_SIZE
        r = random.randint(0, RAND_POSITION)
        self.target_y = r * ELEMENT_SIZE
        self.create_rectangle(self.target_x, self.target_y,
                              self.target_x + DELTA_FOR_BLOCK,
                              self.target_y + DELTA_FOR_BLOCK,
                              fill="yellow", tag="target")

    def onKeyPressed(self, e):
        
        changeSpeed(1, 1)

        key = e.keysym

        if key == "Left" and not self.right:
            self.left = True
            self.up = False
            self.down = False

        if key == "Right" and not self.left:
            self.right = True
            self.up = False
            self.down = False

        if key == "Up" and not self.down:
            self.up = True
            self.right = False
            self.left = False

        if key == "Down" and not self.up:
            self.down = True
            self.right = False
            self.left = False

    def onTimer(self):
        global PAUSE
        if PAUSE is False:

            if self.gameOn:
                self.checkCollisions()
                self.checkTarget()
                self.doMove()
                self.after(DELAY, self.onTimer)

            else:
                self.gameOver()

        else:
            self.after(DELAY, self.onTimer)

    def gameOver(self):

        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,
                         text="Game Over", fill="white")
        updateRatingTable()

    def askColor(self, par):
        if par == "background":
            col = colorchooser.askcolor()[1]
            self.Canvas.configure(bg=col)
        elif par == "target":
            target = self.Canvas.find_withtag("target")
            col = colorchooser.askcolor()[1]
            self.Canvas.itemconfig(target, fill=col)
        elif par == "snake":
            elements = self.Canvas.find_withtag("element")
            col = colorchooser.askcolor()[1]
            for element in elements:
                self.Canvas.itemconfig(element, fill=col)


def changeSpeed(par, delt):
    global DELAY
    
    if par == 1:
        DELAY -= delt
    else:
        DELAY += delt


def pause(par=None):
    global PAUSE
    if PAUSE is True:
        PAUSE = False
    else:
        PAUSE = True


def changeLanguage():
    global LANGUAGE
    if LANGUAGE == 0:

        LANGUAGE = 1

        BACKGROUND_LABEL.set("Background")
        SNAKE_COLOR_LABEL.set("Snake color")
        TARGET_COLOR_LABEL.set("Target color")
        SPEED_PLUS_LABEL.set("Speed +")
        SPEED_MINUS_LABEL.set("Speed -")
        PAUSE_RESUME_LABEL.set("Pause/Resume")
        NEW_GAME_LABEL.set("New game")
        ENG_RUS_LABEL.set("Eng/rus")
        QUIT_LABEL.set("Quit")
    else:
        LANGUAGE = 0
        BACKGROUND_LABEL.set("Цвет фона")
        SNAKE_COLOR_LABEL.set("Цвет змейки")
        TARGET_COLOR_LABEL.set("Цвет цели")
        SPEED_PLUS_LABEL.set("Скорость +")
        SPEED_MINUS_LABEL.set("Скорость -")
        PAUSE_RESUME_LABEL.set("Пауза/возобновить")
        NEW_GAME_LABEL.set("Новая игра")
        ENG_RUS_LABEL.set("Анг/рус")
        QUIT_LABEL.set("Завершить")


class MyApp(Frame):

    def __init__(self, master=None, Title="Змейка"):
        Frame.__init__(self, master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(Title)
        self.grid(sticky="nesw")
        self.create()

    def create(self):
        global COUNT, COUNT_LABEL, PAUSE, DELAY
        COUNT = 0
        DELAY = 120
        updateRatingTable()
        updateRating()

        tmp_label = str(COUNT) + "/" + str(RATING)
        COUNT_LABEL.set(tmp_label)
        self.Canvas = GameBoard(self)
        self.Canvas.grid(row=0, column=0, rowspan=10, sticky="nesw")
        self.Canvas.configure(bg="#1c0b00")

        self.ControlFrame = Frame(self)
        self.ControlFrame.grid(row=0, column=1, sticky="nesw")

        self.ControlFrame.ShowColor = Label(self, bg="#ed125b",
                                            fg="#eee",
                                            textvariable=COUNT_LABEL)
        self.ControlFrame.ShowColor.grid(row=0,
                                         column=1, sticky="nesw")

        self.ControlFrame.AskColor = Button(
                    self,
                    textvariable=BACKGROUND_LABEL,
                    bg="#ffdaa0",
                    command=lambda: GameBoard.askColor(self, "background"))
        self.ControlFrame.AskColor.grid(row=1, column=1, sticky="nesw")

        self.ControlFrame.SnakeColor = Button(
                         self, textvariable=SNAKE_COLOR_LABEL,
                         bg="#ffdaa0",
                         command=lambda: GameBoard.askColor(self, "snake"))
        self.ControlFrame.SnakeColor.grid(row=2, column=1, sticky="nesw")

        self.ControlFrame.TargeColor = Button(
                         self, textvariable=TARGET_COLOR_LABEL,
                         bg="#ffdaa0",
                         command=lambda: GameBoard.askColor(self, "target"))
        self.ControlFrame.TargeColor.grid(row=3, column=1, sticky="nesw")

        self.ControlFrame.SpeedPlus = Button(
                         self, textvariable=SPEED_PLUS_LABEL,
                         bg="#ffdaa0",
                         command=lambda: changeSpeed(1, 50))
        self.ControlFrame.SpeedPlus.grid(row=4, column=1, sticky="nesw")

        self.ControlFrame.SpeedMinus = Button(
                         self, textvariable=SPEED_MINUS_LABEL,
                         bg="#ffdaa0",
                         command=lambda: changeSpeed(0, 50))
        self.ControlFrame.SpeedMinus.grid(row=5, column=1, sticky="nesw")

        self.ControlFrame.PauseResume = Button(
                         self, textvariable=PAUSE_RESUME_LABEL,
                         bg="#ffdaa0",
                         command=lambda: pause())
        self.ControlFrame.PauseResume.grid(row=6, column=1, sticky="nesw")

        self.ControlFrame.PauseResume = Button(
                         self, textvariable=NEW_GAME_LABEL,
                         bg="#ffdaa0",
                         command=self.newGame)
        self.ControlFrame.PauseResume.grid(row=7, column=1, sticky="nesw")

        self.ControlFrame.PauseResume = Button(
                         self, textvariable=ENG_RUS_LABEL,
                         bg="#ffdaa0",
                         command=lambda: changeLanguage())
        self.ControlFrame.PauseResume.grid(row=8, column=1, sticky="nesw")

        self.ControlFrame.Quit = Button(
                         self, textvariable=QUIT_LABEL,
                         bg="#ffdaa0", command=self.quit)
        self.ControlFrame.Quit.grid(row=9, column=1, sticky="nesw")

    def newGame(self, par=None):

        self.create()


app = MyApp(tk)
tk.bind("<space>", pause)
tk.bind("<q>", quit)
app.mainloop()
