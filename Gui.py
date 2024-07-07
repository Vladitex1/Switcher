from tkinter import *
from tkinter import font as f

import multiprocessing

import Switcher


class GUI:

    def __init__(self):

        self.General()

    def General(self):

        root = Tk()
        root.title("Фон окна")
        root.geometry("400x300")
        root.resizable(width=True, height=True)


        font = f.Font(family="Aboreto", size=11, weight="bold", slant="italic")
        self.status = Label(height=5,text="Status",font=font)
        self.label = Label(height=2,text="-",font=font)

        #Подключение надписей
        self.status.pack()
        self.label.pack()

        #Кнопки
        btn_on = Button(root, text="Включить", command=self.TurnON)  # включение
        btn_off = Button(root, text="Выключить", command=self.TurnOFF)  # выключение
        btn_on.place(x=110, y=150)
        btn_off.place(x=210, y=150)

        root.mainloop()

        #if keyboard.is_pressed("F11"):

    def TurnON(self):
        global stat
        on = "Включено"
        self.label.configure(text=on)

    def TurnOFF(self):
        global stat
        off = "Выключено"
        self.label.configure(text=off)

    def ProgramStart(self):
        print("ITS ALIVE!!!")
        #Switcher.Program()

if __name__ == '__main__':
    GUI()
