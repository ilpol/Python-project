#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
import random

from tkinter import Tk, Frame, Canvas, ALL, Label, Button, StringVar, Entry
from tkinter import colorchooser

import os
import sys
import xml.etree.ElementTree as ET

tk = Tk()

DELTA_FOR_BLOCK = 4
WIDTH = 300
HEIGHT = 300
DELAY = 120
ELEMENT_SIZE = 10
ALL_ELEMENTS = WIDTH * HEIGHT / (ELEMENT_SIZE * ELEMENT_SIZE)
RAND_POSITION = 27

COUNT_LABEL = StringVar()
RATING_LABEL = StringVar()
NAME = StringVar()

COUNT = 0
CUR_RATING = 0
RATING = 10
XMLRATING = None
PATH = os.path.dirname(sys.argv[0])
RATING_FILE = os.path.join(PATH, 'rating.xml')
PAUSE = False

rating_list = {}

colors = {'fg': 'black',
          'fgscore': 'white',
          'bgbutton': '#ffdaa0',
          'bgcanvas': '#1c0b00',
          'bgscore': '#ed125b'}

gettext.install('snake', os.path.join(os.path.dirname(__file__), 'locale'))

'''
Игра "Змейка"

Чтобы сгенерировать документацию надо выполнить команду

    pydoc -w snake
'''


def updateRatingTable(score, name):
    """
    Обновляет рейтенговую таблицу

    :param score: Счет игрока
    :param name: Имя игрока
    :return: ничего не возвращает
    """
    global rating_list, XMLRATING

    for i in range(10, 0, -1):
        if CUR_RATING == i:
            rating_list[i] = name + ':' + str(score)
        elif CUR_RATING < i:
            rating_list[i + 1] = rating_list[i]
    if len(rating_list) == 11:
        rating_list.pop(11)

    root = ET.Element('rating_table')
    rating = {}
    place = {}
    name = {}
    value = {}

    for i in range(10):
        divider = rating_list[i + 1].find(':')
        rating[i] = ET.SubElement(root, 'rating')
        place[i] = ET.SubElement(rating[i], 'place')
        place[i].text = str(i + 1)
        name[i] = ET.SubElement(rating[i], 'name')
        name[i].text = (rating_list[i + 1])[:divider]
        value[i] = ET.SubElement(rating[i], 'value')
        value[i].text = (rating_list[i + 1])[(divider + 1):]

    tree = ET.ElementTree(root)
    tree.write(RATING_FILE, encoding='utf-8')


def loadRating():
    """
    Загружает рейтенговую таблицу

    :return: ничего не возвращает
    """
    global rating_list, XMLRATING

    if not os.path.isfile(RATING_FILE):

        root = ET.Element('rating_table')
        rating = {}
        place = {}
        name = {}
        value = {}

        for i in range(10):
            rating[i] = ET.SubElement(root, 'rating')
            place[i] = ET.SubElement(rating[i], 'place')
            place[i].text = str(i + 1)
            name[i] = ET.SubElement(rating[i], 'name')
            name[i].text = 'Test' + str(i + 1)
            value[i] = ET.SubElement(rating[i], 'value')
            value[i].text = str(10 - i)

        tree = ET.ElementTree(root)
        tree.write(RATING_FILE, encoding='utf-8')

    xmltree = ET.parse(RATING_FILE)
    XMLRATING = xmltree.getroot()

    rating_list = {}

    for rating in XMLRATING:
        place = 0
        value = 0
        rating_value = ''
        for item in rating:
            if item.tag == 'place':
                place = int(item.text)
            if item.tag == 'value':
                value = item.text
            if item.tag == 'name':
                rating_value = str(item.text) + ':'
        rating_value += str(value)
        rating_list[place] = rating_value


def updateRating():
    """
    Обновляет рейтинг игрока

    :return: ничего не возвращает
    """
    global score_list, COUNT, RATING, CUR_RATING

    if CUR_RATING != 0:
        rating_list[CUR_RATING] = rating_list[CUR_RATING].replace('* ', '')

    if not rating_list:
        CUR_RATING = 0
    else:
        for i in range(10):
            divider = rating_list[i + 1].find(':')
            if COUNT >= int((rating_list[i + 1])[(divider + 1):]):
                CUR_RATING = i + 1
                break
    if CUR_RATING != 0:
        rating_list[CUR_RATING] = '* ' + rating_list[CUR_RATING]

    tmp_label = _("Rating:") + '\n'
    for i in range(10):
        tmp_label += rating_list[i + 1] + '\n'
    RATING_LABEL.set(tmp_label)


loadRating()
updateRating()


class popupWindow(Frame):
    """
    Всплывающее окно после проигрыша

    :param Frame: наследует класс Frame
    """
    def __init__(self, master=None, Title=_("Congratulations!")):
        """
        Заполняет параметры всплывающего окна

        :param self: Ссылка на себя
        :param master: Ссылка на родителя
        :param Title: Заголовок
        :return: ничего не возвращает
        """
        Frame.__init__(self, master)

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(Title)
        self.grid(sticky='nesw')
        self.label1 = Label(self, text=_("You broke some records!"),
                            bg=colors['bgbutton'], fg=colors['fg'])
        self.label1.grid(row=0, column=0, sticky='nesw')
        self.label2 = Label(self, text=_("Please, enter your name:"),
                            bg=colors['bgbutton'], fg=colors['fg'])
        self.label2.grid(row=1, column=0, sticky='nesw')

        self.name = Entry(self, bg=colors['bgscore'], fg=colors['fgscore'])
        self.name.grid(row=2, column=0, sticky='nesw')

        self.ok = Button(self, text='Ok', bg=colors['bgbutton'],
                         fg=colors['fg'], command=self.cleanup)
        self.ok.grid(row=3, column=0, sticky='nesw')

    def cleanup(self):
        """
        Уничтожает всплывающее окно

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        global NAME
        NAME = self.name.get()
        self.master.destroy()


class GameBoard(Canvas):
    """
    Игровое поле

    :param Canvas: наследует класс Canvas
    """
    def __init__(self, master):
        """
        Вызывает конструктор родительского класса и функцию,
        инициализирующую объекты на игровом поле

        :param self: Ссылка на себя
        :param master: Ссылка на родителя
        :return: ничего не возвращает
        """

        self.master = master
        Canvas.__init__(self, master,
                        width=WIDTH,
                        height=HEIGHT)
        self.init()

    def init(self):
        """
        Инициализирует объекты на игровом поле

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        global LANGUAGE

        loadRating()
        updateRating()

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
        self.bind_all('<Key>', self.onKeyPressed)
        self.after(DELAY, self.onTimer)

    def popup(self):
        """
        Вызывает всплывающее окно

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        tkpopup = Tk()
        self.popupWindow = popupWindow(tkpopup)
        tkpopup.wait_window(self.popupWindow)

    def createObjects(self):
        """
        Создает объекты на игровом поле

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        self.create_rectangle(self.target_x, self.target_y,
                              self.target_x + 4, self.target_y + 4,
                              fill='yellow', tag='target')

        self.create_rectangle(50, 50, 50 + DELTA_FOR_BLOCK,
                              50 + DELTA_FOR_BLOCK, fill='red', tag='head')
        self.create_rectangle(30, 50, 30 + DELTA_FOR_BLOCK,
                              50 + DELTA_FOR_BLOCK, fill='orange',
                              tag='element')
        self.create_rectangle(40, 50, 40 + DELTA_FOR_BLOCK,
                              50 + DELTA_FOR_BLOCK, fill='orange',
                              tag='element')

    def checkTarget(self):
        """
        Проверяет, достигнула ли змейка цели

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        global COUNT, COUNT_LABEL

        target = self.find_withtag('target')
        head = self.find_withtag('head')

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for ovr in overlap:

            if target[0] == ovr:
                COUNT += 1
                updateRating()
                tmp_label = _("Scores:") + '\n' + str(COUNT)
                COUNT_LABEL.set(tmp_label)

                x = self.coords(target)[0]
                y = self.coords(target)[1]
                self.create_rectangle(x, y,
                                      x + DELTA_FOR_BLOCK,
                                      y + DELTA_FOR_BLOCK,
                                      fill='orange', tag='element')
                self.locateTarget()

    def doMove(self):
        """
        Делает движение всех элементвов змейки на один шаг

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """

        elements = self.find_withtag('element')
        head = self.find_withtag('head')

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
        """
        Проверяет, столкнулась ли змейка со стенами или сама с собой

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """

        elements = self.find_withtag('element')
        head = self.find_withtag('head')

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
        """
        Генерирует местоположение цели

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """

        target = self.find_withtag('target')
        self.delete(target[0])

        r = random.randint(0, WIDTH // ELEMENT_SIZE)
        self.target_x = r * ELEMENT_SIZE
        if (self.target_x != 0):
            self.target_x = self.target_x - ELEMENT_SIZE

        r = random.randint(0, HEIGHT // ELEMENT_SIZE)

        self.target_y = r * ELEMENT_SIZE
        if (self.target_y != 0):
            self.target_y = self.target_y - ELEMENT_SIZE

        self.create_rectangle(self.target_x, self.target_y,
                              self.target_x + DELTA_FOR_BLOCK,
                              self.target_y + DELTA_FOR_BLOCK,
                              fill='yellow', tag='target')

    def onKeyPressed(self, e):
        """
        Реагирует на нажатие кнопок и изменяет направление движения
        змейки

        :param self: Ссылка на себя
        :param е: кнопка
        :return: ничего не возвращает
        """
        changeSpeed(1, 1)

        key = e.keysym

        if key == 'Left' and not self.right:
            self.left = True
            self.up = False
            self.down = False

        if key == 'Right' and not self.left:
            self.right = True
            self.up = False
            self.down = False

        if key == 'Up' and not self.down:
            self.up = True
            self.right = False
            self.left = False

        if key == 'Down' and not self.up:
            self.down = True
            self.right = False
            self.left = False

    def onTimer(self):
        """
        После задержки обновляет состояние поля, проверяет столкновения
        и снова вызывает себя после задержки

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        global PAUSE, WIDTH, HEIGHT
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

        WIDTH = self.winfo_width() - 2
        HEIGHT = self.winfo_height() - 2

    def gameOver(self):
        """
        Вызывается после проигрыша. Обновляет рейтенговую таблицу,
        очищает поле и выводит тект "Игра окончена"

        :param self: Ссылка на себя
        :return: ничего не возвращает
        """
        global COUNT

        if CUR_RATING <= 10 and CUR_RATING >= 1:
            self.popup()
            updateRatingTable(COUNT, NAME)

        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,
                         text=_("Game Over"), fill='white')

    def askColor(self, par):
        """
        Изменяет цвет фона, цели или элементов змейки

        :param self: Ссылка на себя
        :param par: параметр определяет, изменять ли цвет фона, цели
        или элементов змейки
        :return: ничего не возвращает
        """
        if par == 'background':
            col = colorchooser.askcolor()[1]
            self.Canvas.configure(bg=col)
        elif par == 'target':
            target = self.Canvas.find_withtag('target')
            col = colorchooser.askcolor()[1]
            self.Canvas.itemconfig(target, fill=col)
        elif par == 'snake':
            elements = self.Canvas.find_withtag('element')
            col = colorchooser.askcolor()[1]
            for element in elements:
                self.Canvas.itemconfig(element, fill=col)


def changeSpeed(par, delt):
    """
    Увеличивает или уменьшает скорость игры

    :param delt: определяет, на какую величину увеличивать или уменьшать
    задержку
    :return: ничего не возвращает
    """

    global DELAY

    if par == 1:
        DELAY -= delt
    else:
        DELAY += delt


def pause(par=None):
    """
    Ставит игру на паузу

    :return: ничего не возвращает
    """
    global PAUSE
    if PAUSE is True:
        PAUSE = False
    else:
        PAUSE = True


class MyApp(Frame):
    """
    Класс игры. Создает все окна и инициализирует игру

    :param Frame: Наследуется от класса Frame
    :return: ничего не возвращает
    """

    def __init__(self, master=None, Title=_("Snake")):
        """
        Инициализирует параметры окна, вызывает функцию, заполняющую
        параметры игры

        :param self: ссылка на себя
        :param master: ссылка на родителя
        :param Title: заголовок
        :return: ничего не возвращает
        """
        Frame.__init__(self, master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.title(Title)
        self.grid(sticky='nesw')
        self.create()

    def create(self):
        """
        Инициализирует создает кнопки, игровое поле, вызывает функцию,
        инициализирущую параметры и игры и запускающую ее

        :param self: ссылка на себя
        :return: ничего не возвращает
        """
        global COUNT, COUNT_LABEL, PAUSE, DELAY
        global CUR_RATING, RATING_LABEL, rating_list
        COUNT = 0
        DELAY = 120
        CUR_RATING = 0
        loadRating()
        updateRating()

        tmp_label = _("Rating:") + '\n'
        for i in range(10):
            tmp_label += rating_list[i + 1] + '\n'
        RATING_LABEL.set(tmp_label)

        self.ControlFrame = Frame(self)
        self.ControlFrame.grid(row=0, column=2, sticky='nesw')

        self.ControlFrame.Tmp = Label(
            self, bg=colors['bgbutton'],
            fg=colors['fg'], textvariable=RATING_LABEL, width=10)
        self.ControlFrame.Tmp.grid(
            row=0, column=0,
            rowspan=10, sticky='nesw')

        self.Canvas = GameBoard(self)
        self.Canvas.grid(row=0, column=1, rowspan=10, sticky='nesw')
        self.Canvas.configure(bg=colors['bgcanvas'])

        tmp_label = _("Scores:") + '\n' + str(COUNT)
        COUNT_LABEL.set(tmp_label)

        self.ControlFrame.ShowColor = Label(
            self, bg=colors['bgscore'],
            fg=colors['fgscore'], textvariable=COUNT_LABEL)
        self.ControlFrame.ShowColor.grid(row=0, column=2, sticky='nesw')

        self.ControlFrame.AskColor = Button(
            self, text=_("Background color"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=lambda: GameBoard.askColor(self, 'background'))
        self.ControlFrame.AskColor.grid(row=1, column=2, sticky='nesw')

        self.ControlFrame.SnakeColor = Button(
            self, text=_("Snake color"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=lambda: GameBoard.askColor(self, 'snake'))
        self.ControlFrame.SnakeColor.grid(row=2, column=2, sticky='nesw')

        self.ControlFrame.TargeColor = Button(
            self, text=_("Target color"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=lambda: GameBoard.askColor(self, 'target'))
        self.ControlFrame.TargeColor.grid(row=3, column=2, sticky='nesw')

        self.ControlFrame.SpeedPlus = Button(
            self, text=_("Speed +"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=lambda: changeSpeed(1, 50))
        self.ControlFrame.SpeedPlus.grid(row=4, column=2, sticky='nesw')

        self.ControlFrame.SpeedMinus = Button(
            self, text=_("Speed -"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=lambda: changeSpeed(0, 50))
        self.ControlFrame.SpeedMinus.grid(row=5, column=2, sticky='nesw')

        self.ControlFrame.PauseResume = Button(
            self, text=_("Pause/Resume"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=lambda: pause())
        self.ControlFrame.PauseResume.grid(row=6, column=2, sticky='nesw')

        self.ControlFrame.PauseResume = Button(
            self, text=_("New game"),
            bg=colors['bgbutton'], fg=colors['fg'],
            command=self.newGame)
        self.ControlFrame.PauseResume.grid(row=7, column=2, sticky='nesw')

        self.ControlFrame.Quit = Button(
            self, text=_("Quit"),
            bg=colors['bgbutton'], fg=colors['fg'], command=self.quit)
        self.ControlFrame.Quit.grid(row=8, column=2, sticky='nesw')

    def newGame(self, par=None):
        """
        Создает новую игру

        :param self: ссылка на себя
        :return: ничего не возвращает
        """

        self.create()


if __name__ == '__main__':
    app = MyApp(tk)
    tk.bind('<space>', pause)
    tk.bind('<q>', quit)
    app.mainloop()
