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
        #self.init()


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

app = MyApp(tk)
tk.bind("<space>", pause)
tk.bind("<q>", quit)
app.mainloop()