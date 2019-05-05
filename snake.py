#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW, Label,Button, StringVar
from tkinter import colorchooser



DELTA_FOR_BLOCK = 4
WIDTH = 300
HEIGHT = 300
DELAY = 120
ELEMENT_SIZE = 10
ALL_ELEMENTS = WIDTH * HEIGHT / (ELEMENT_SIZE * ELEMENT_SIZE)
RAND_POSITION = 27
tk = Tk()

COUNT_LABEL= StringVar()

COUNT = 0
RATING = 1
PAUSE = False
score_list = []

def update_rating_table():
    global score_list
    f=open("rating.txt", "r")
    contents =f.read()
    score_list = []
    for score in contents.split("\n"):
        if score != "":
          score_list.append(int(score))
    score_list.append(COUNT)
    #удаляем повторения
    score_list = list(set(score_list))
    score_list.sort(reverse = True)
    if len(score_list)> 9:
        score_list = score_list[:9]
    f.close()
    f=open("rating.txt", "w")
    for score in score_list:
        f.write(str(score) + "\n")
    f.close()

def update_rating():
    global score_list
    global RATING
    cur_rating = 1
    if not score_list:
        RATING = 1
    else:
        for score in score_list:
            if COUNT > score:
                break
            else:
                cur_rating +=1

    RATING = cur_rating
    tmp_label = str(COUNT) + "/" + str(RATING)
    COUNT_LABEL.set(tmp_label)

update_rating_table()
update_rating()

class GameBoard(Canvas):
    def __init__(self, master):
        
        Canvas.__init__(self, master,width=WIDTH, height=HEIGHT)
        self.init()
    def init(self):

        update_rating_table()
        update_rating()

        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.gameOn = True
        self.elements = 3

        self.target_x = 100
        self.target_y = 190

        






        self.focus_get()

        self.createObjects()
        self.locateTarget()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(DELAY, self.onTimer)
    
    def createObjects(self):
        self.create_rectangle(self.target_x, self.target_y,self.target_x + 4, self.target_y + 4, 
                                  fill = "yellow", tag="target")
        
        self.create_rectangle(50, 50, 50 + DELTA_FOR_BLOCK, 
                                    50 + DELTA_FOR_BLOCK, fill = "red", tag="head")
        self.create_rectangle(30, 50, 30 + DELTA_FOR_BLOCK, 
                                     50 + DELTA_FOR_BLOCK, fill = "orange", tag="element")
        self.create_rectangle(40, 50, 40+ DELTA_FOR_BLOCK,
                                     50+ DELTA_FOR_BLOCK, fill = "orange", tag="element")
       


    def checkTarget(self):
        global COUNT,COUNT_LABEL

        target = self.find_withtag("target")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if target[0] == ovr:
                COUNT +=1
                update_rating()
                tmp_label = str(COUNT) + "/" + str(RATING)
                COUNT_LABEL.set(tmp_label)
                
                x = self.coords(target)[0]
                y = self.coords(target)[1]
                self.create_rectangle(x, y, x + DELTA_FOR_BLOCK, y + DELTA_FOR_BLOCK
                                           , fill = "orange", tag="element")
                self.locateTarget()

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
                                   self.target_x + DELTA_FOR_BLOCK, self.target_y + DELTA_FOR_BLOCK, 
                                  fill = "yellow", tag="target")


    def onTimer(self):
        global PAUSE
        if PAUSE == False:

          if self.gameOn:
            self.checkCollisions()
            self.checkTarget()
            self.doMove()
            self.after(DELAY, self.onTimer)

          else:
            self.gameOver()

        else:
          self.after(DELAY, self.onTimer)


    def askColor(self,par):
        if par == "background":
            col = colorchooser.askColor()[1]
            self.Canvas.configure(bg=col)
        elif par == "target":
            target = self.Canvas.find_withtag("target")
            col = colorchooser.askColor()[1]            
            self.Canvas.itemconfig(target, fill=col)
        elif par == "snake":
            elements = self.Canvas.find_withtag("element")
            col = colorchooser.askColor()[1]
            for element in elements:
                self.Canvas.itemconfig(element, fill=col)

        


def pause (par = None):
    global PAUSE
    if PAUSE == True:
        PAUSE = False
    else:
        PAUSE = True

        
class MyApp(Frame):        

    def __init__(self, master=None, Title="Змейка"):
        Frame.__init__(self, master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(Title)
        self.grid(sticky="nesw")
        #self.create()



    def create(self):
        global COUNT,COUNT_LABEL,PAUSE
        COUNT = 0
        update_rating_table()
        update_rating()
        
        tmp_label = str(COUNT) + "/" + str(RATING)
        COUNT_LABEL.set(tmp_label)
        self.Canvas = GameBoard(self)
        self.Canvas.grid(row=0, column=0,rowspan = 9, sticky="nesw")
        self.Canvas.configure(bg="#1c0b00")

        

        self.ControlFrame = Frame(self)
        self.ControlFrame.grid(row=0, column=1,  sticky="nesw")


        self.ControlFrame.ShowColor = Label(self, bg = "#ed125b",fg="#eee",textvariable=COUNT_LABEL)
        self.ControlFrame.ShowColor.grid(row=0, column=1, sticky="nesw")

        self.ControlFrame.AskColor = Button(self, text="Цвет фона",bg="#ffdaa0",
                                                  command=lambda:GameBoard.askColor(self,"background"))
        self.ControlFrame.AskColor.grid(row=1, column=1, sticky="nesw")

        

        self.ControlFrame.SnakeColor = Button(self, text="Цвет змейки",bg="#ffdaa0"
                                                   ,command=lambda:GameBoard.askColor(self,"snake"))
        self.ControlFrame.SnakeColor.grid(row=2, column=1, sticky="nesw")

        self.ControlFrame.TargeColor = Button(self, text="Цвет цели",
                                                   bg="#ffdaa0",command=lambda:GameBoard.askColor(self,"target"))
        self.ControlFrame.TargeColor.grid(row=3, column=1, sticky="nesw")

        self.ControlFrame.SpeedPlus = Button(self, text="Скорость +",bg="#ffdaa0"
                                                ,command= lambda: change_speed(1))
        self.ControlFrame.SpeedPlus.grid(row=4, column=1, sticky="nesw")

        self.ControlFrame.SpeedMinus = Button(self, text="Скорость -",bg="#ffdaa0"
                                                 ,command= lambda: change_speed(0))
        self.ControlFrame.SpeedMinus.grid(row=5, column=1, sticky="nesw")

app = MyApp(tk)
tk.bind("<space>", pause)
tk.bind("<q>", quit)
app.mainloop()