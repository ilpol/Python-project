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

class GameBoard(Canvas):
    def __init__(self, master):
        
        Canvas.__init__(self, master,width=WIDTH, height=HEIGHT)
        #self.init()


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