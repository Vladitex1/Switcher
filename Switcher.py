import win32gui as w32g
import win32api as w32a
import win32con as w32c
from win32api import EnumDisplayMonitors, GetMonitorInfo
import keyboard
import time
import pystray
import PIL.Image
from plyer import notification


image = PIL.Image.open("icon.ico")

ExitProgram = False
Run = True
NotifyON = False

# width - ширина

class Program:
    WindowID = []

    def __init__(self):
        Optimise = Optimisation()
        Windows1ResWidth, Windows1ResHeight, Windows2ResWidth, Windows2ResHeight = Optimise.WindowOption()

        self.Scr1w = int(Windows1ResWidth / 2)
        self.Scr1h = int(Windows1ResHeight / 2)
        self.Scr2w = int(Windows2ResWidth - Windows2ResWidth / 4)
        self.Scr2h = int(Windows2ResHeight - self.Scr1h)

    # Служебные

    def MouseClick(self):
        w32a.mouse_event(w32c.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.01)
        w32a.mouse_event(w32c.MOUSEEVENTF_LEFTUP, 0, 0)

    def WindowEquip(self, left, right):
        Program.WindowID = []
        if left:
            w32a.SetCursorPos((self.Scr1w, self.Scr1h))
            self.MouseClick()
            self.WindowID.append(w32g.GetForegroundWindow())

        if right:
            w32a.SetCursorPos((self.Scr2w, self.Scr2h))
            self.MouseClick()
            self.WindowID.append(w32g.GetForegroundWindow())

    def ProgramStop(self):
        global Run
        Run = False
        if NotifyON:
            notification.notify(title='Switcher', message='Выключение программы', app_name='Switcher', app_icon='icon.ico',
                                timeout=3)

# Работа с окнами
class Window:

    def Switch(self):
        Prog = Program()
        if NotifyON:
            notification.notify(title='Switcher', message=' <---> ', app_name='Switcher', app_icon='icon.ico',
                                timeout=2)
        MouseSave = w32g.GetCursorPos()
        Prog.WindowEquip(True, True)
        w32g.MoveWindow(Prog.WindowID[1], 0, 0, 1920, 1080, 0)
        w32g.MoveWindow(Prog.WindowID[0], 1920, 0, 1920, 1080, 0)
        w32g.SetForegroundWindow(Prog.WindowID[1])
        w32a.SetCursorPos(MouseSave)
        Prog.WindowID = []
        Prog.MouseClick()

    def SwitchLeftToRight(self):
        Prog = Program()
        if NotifyON:
            notification.notify(title='Switcher', message=' ---> ', app_name='Switcher', app_icon='icon.ico',
                                timeout=2)
        MouseSave = w32g.GetCursorPos()
        Prog.WindowEquip(True, False)
        w32g.MoveWindow(Prog.WindowID[0], 1920, 0, 1920, 1080, 0)
        w32g.SetForegroundWindow(Prog.WindowID[0])
        w32a.SetCursorPos(MouseSave)
        Prog.MouseClick()
        Prog.WindowID = []

    def SwitchRightToLeft(self):
        Prog = Program()
        if NotifyON:
            notification.notify(title='Switcher', message=' <--- ', app_name='Switcher', app_icon='icon.ico',
                                timeout=2)
        MouseSave = w32g.GetCursorPos()
        Prog.WindowEquip(False, True)
        w32g.MoveWindow(Prog.WindowID[0], 0, 0, 1920, 1080, 0)
        w32g.SetForegroundWindow(Prog.WindowID[0])
        w32a.SetCursorPos(MouseSave)
        Prog.MouseClick()
        Prog.WindowID = []


# Трей
class Tray:
    def Inclusion(self):
        self.Tray = pystray.Icon(name="Switcher", icon=image, title="Switcher by Vladitex1 ;)", menu=pystray.Menu(
            pystray.MenuItem('Поменять местами окна', Tray.Switch),
            pystray.MenuItem('Передвинуть --->', Window.SwitchLeftToRight),
            pystray.MenuItem('Передвинуть <---', Window.SwitchRightToLeft),
            pystray.MenuItem('Проверить статус', Tray.Status),
            pystray.MenuItem('Выход', self.Stop)
        ))
        self.Tray.run_detached()

    def Switch(self):
        Window().Switch()

    def Stop(self):
        self.Tray.stop()
        Program().ProgramStop()

    def Status(self):
        notification.notify(title='Switcher', message='Программа работает', app_name='Switcher', app_icon='icon.ico', timeout=3)


# Оптимизация
class Optimisation:

    def WindowOption(self):
        MonitorsData = []
        temp = []

        for monitor in EnumDisplayMonitors():
            monitor_info = GetMonitorInfo(monitor[0])
            try:
                for i in range(10):
                    if monitor_info['Flags'] == i:
                        temp.append(i)

            except ZeroDivisionError:
                print("error: Monitor Not Found")

        MaxMonit = len(temp)

        for monitor in EnumDisplayMonitors():
            monitor_info = GetMonitorInfo(monitor[0])
            for i in range(MaxMonit):
                if monitor_info['Flags'] == i:
                    MonitorInformation = monitor_info.get("Work")

                    Width = MonitorInformation[2]
                    Height = MonitorInformation[3]

                    temp = [Width, Height]

                    MonitorsData.append(temp)

        del temp
        return MonitorsData[1][0], MonitorsData[1][1], MonitorsData[0][0], MonitorsData[0][1]

def Running():

    Program()
    Brain = Program()
    Win = Window()
    tray = Tray()
    tray.Inclusion()

    while Run:
        time.sleep(.1)


        # Служебные
        # Выключение программы
        if keyboard.is_pressed('Ctrl+F11'):
            try:
                tray.Stop()
            except AttributeError:
                Brain.ProgramStop()

        # Проверка работы программы
        if keyboard.is_pressed('Ctrl+F9'):
            notification.notify(title='Switcher', message='Программа работает', app_name='Switcher', app_icon='icon.ico', timeout=1)

        # Поменять окна местами
        if keyboard.is_pressed('Ctrl+F10'):
            Win.Switch()

        # Перевод левого окна вправо
        if keyboard.is_pressed('Ctrl+F5'):
            Win.SwitchLeftToRight()

        # Перевод правого окна влево
        if keyboard.is_pressed('Ctrl+F6'):
            Win.SwitchRightToLeft()



if __name__ == '__main__':
    Running()
