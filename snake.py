#!/usr/bin/env python3


from tkinter import *

class App(Frame):

    def __init__(self, master=None, Title="Application"):
        Frame.__init__(self, master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(Title)
        self.grid(sticky=N+E+S+W)
        self.create()
        

    def create(self):
      pass

    
        
class Paint(Canvas):


    def __init__(self, master=None, *ap, foreground="black", **an):
        self.foreground = StringVar()
        self.foreground.set(foreground)
        Canvas.__init__(self, master, *ap, **an)


class MyApp(App):



    def create(self):
        self.Canvas = Paint(self)
        self.Canvas.grid(row=0, column=0,rowspan = 9, sticky=N+E+S+W)
        self.Canvas.configure(bg="#ffdaa0")

        

        self.ControlFrame = Frame(self)
        self.ControlFrame.grid(row=0, column=1,  sticky=N+E+S+W)

        self.ControlFrame.ShowColor = Label(self, bg = "#ed125b",fg="#eee",text="Счет")
        self.ControlFrame.ShowColor.grid(row=0, column=1, sticky=N+E+S+W)

        self.ControlFrame.AskColor = Button(self, text="Цвет фона")
        self.ControlFrame.AskColor.grid(row=1, column=1, sticky=N+E+S+W)

        

        self.ControlFrame.Copy1 = Button(self, text="Цвет змейки")
        self.ControlFrame.Copy1.grid(row=2, column=1, sticky=N+E+S+W)

        self.ControlFrame.Copy1 = Button(self, text="Цвет цели")
        self.ControlFrame.Copy1.grid(row=3, column=1, sticky=N+E+S+W)

        self.ControlFrame.Clear1 = Button(self, text="Скорость")
        self.ControlFrame.Clear1.grid(row=4, column=1, sticky=N+E+S+W)

        self.ControlFrame.Clear2 = Button(self, text="Завершить")
        self.ControlFrame.Clear2.grid(row=5, column=1, sticky=N+E+S+W)

        



app = MyApp(Title="Змейка")
app.mainloop()
for item in app.Canvas.find_all():
    print(*app.Canvas.coords(item), app.Canvas.itemcget(item, "fill"))

