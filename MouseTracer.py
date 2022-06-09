import pyautogui
import time
import keyboard
import numpy as np


class MouseOperation:

    def click(self):
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        pass

    def doubleClick(self):
        self.click()
        self.click()
        pass

    COUNTER = 0
    mementoList = []
    DELAY = 0
    cur_MouseX, cur_MouseY = 0, 0

    def Operation(self):
        pass

    def createMemento(self):
        mouse_memento = MouseMemento(
            self.COUNTER, self.cur_MouseX, self.cur_MouseY, self.DELAY)
        return mouse_memento.returnToList()

    def printMemento(self):
        npMemento = np.array(self.mementoList)
        print('(INDEX - X - Y - DELAY)')
        print(npMemento)
        self.selectOperate()

    def selectOperate(self):
        print("F4 TO START OPRATION MOD")
        print("F5 TO MODIFY MOD")
        print()
        while True:
            if keyboard.read_key() == "f4":
                self.operateMemento()
            if keyboard.read_key() == "f5":
                self.modifyMemento()

    def modifyMemento(self):
        print("MODIFY MOD ACTIVATED")
        print("PLEASE INPUT INDEX NUMBER TO MODIFY", end="\n\n")
        idx = int(input())
        print("MODIFY", idx, "INDEX. WHAT WOULD YOU LIKE TO CHANGE?")
        print("1. DELETE    2. CHANGE")
        if int(input()) == 1:
            np.delete(self.mementoList, np.where(
                self.mementoList[:][0] == idx - 1))
        self.printMemento()
        

    def operateMemento(self):
        print("OPERATION MODE ACTIVATED")
        print('PLEASE INPUT REPEAT COUNTER')
        repeat = int(input())
        self.mementoList[0][3] = 1000
        self.click()
        for _ in range(repeat):
            for memento in self.mementoList:
                xpos = memento[1]
                ypos = memento[2]
                delay = memento[3] / 1000.0

                pyautogui.moveTo(xpos, ypos)
                self.click()
                time.sleep(delay)
        print('REPEAT COMPLETE')

        self.selectOperate()


class MouseMemento:  # memento pattern
    def __init__(self, counter, x, y, delay):
        self.counter = counter
        self.x = x
        self.y = y
        self.delay = delay

    def returnToList(self):
        historyList = [self.counter - 1, self.x, self.y, self.delay]
        return historyList


def selectMode(inputStr) -> MouseOperation:
    if inputStr == 'click':
        print('CLICK MOD OPRATION')
        print('PRESS F1 TO RECORD AND CLICK')
        print('PRESS F2 TO STOP AND PRINT RECORDED HISTORY')
        return clickRecord()
    elif inputStr == 'non-click':
        print('NON-CLICK MOD OPRATION')
        print('PRESS F1 TO RECORD')
        print('PRESS F2 TO STOP AND PRINT RECORDED HISTORY')
        return locationRecord()


class clickRecord(MouseOperation):
    def Operation(self):
        timer_start = time.time()
        while True:
            self.cur_MouseX, self.cur_MouseY = pyautogui.position()
            if keyboard.read_key() == "f1":
                self.COUNTER += 1
                pyautogui.mouseDown()
                pyautogui.mouseUp()

                print(self.COUNTER, "CLICK LOCATION =  X :",
                      self.cur_MouseX, " Y :", self.cur_MouseY)
                timer_end = time.time()
                self.DELAY = int((timer_end - timer_start)*1000)

                timer_start = timer_end
                print("DELAY : ", int(self.DELAY), "ms")

                self.mementoList.append(self.createMemento())

            if keyboard.read_key() == "f2":
                self.printMemento()
                break

            # if keyboard.read_key() == "f3": 되돌리는 기능 추가


class locationRecord(MouseOperation):
    def Operation(self):
        timer_start = time.time()
        while True:
            self.cur_MouseX, self.cur_MouseY = pyautogui.position()
            if keyboard.read_key() == "f1":
                self.COUNTER += 1
                print("CURRENT LOCATION =  X :",
                      self.cur_MouseX, " Y :", self.cur_MouseY)
                timer_end = time.time()
                self.DELAY = int((timer_end - timer_start)*1000)
                timer_start = timer_end
                print("DELAY : ", int(self.DELAY), "ms")
                self.mementoList.append(self.createMemento())

            if keyboard.read_key() == "f2":
                self.printMemento()
                self.selectOperate()
                break


class Lobby:  # command pattern
    def Intro(self):
        print("************************")
        print("*         HUFS         *")
        print("*    DESIGN PATTERN    *")
        print("*     TERM PROJECT     *")
        print("*     BY 201801190     *")
        print("*                      *")
        print("*  MOUSE CLICK TRACER  *")
        print("*        v 1.0         *")
        print("*                      *")
        print("************************")
        print()

    def printMod(self):
        print("************************")
        print("*                      *")
        print("*    ENTER CLICK MOD   *")
        print("*                      *")
        print("*   1. CLICK MOD       *")
        print("*   2. NON-CLICK MOD   *")
        print("*                      *")
        print("************************")
        print()

    def selectMod(self):
        modNumber = int(input())
        if modNumber == 1:  # strategy pattern
            mouseOP = selectMode('click')
            mouseOP.Operation()
        elif modNumber == 2:
            mouseOP = selectMode('non-click')
            mouseOP.Operation()

        else:
            print('ERROR : PLEASE ENTER A VAILD NUMBER')
            self.selectMod()


class Mod:
    def execute(self):
        pass


class ModCommand(Mod):
    def __init__(self, lobby: Lobby, commands: list[str]):
        self.lobby = lobby
        self.commands = commands

    def execute(self):
        for commands in self.commands:
            if commands == 'Intro':
                self.lobby.Intro()
            elif commands == 'printMod':
                self.lobby.printMod()
            elif commands == 'selectMod':
                self.lobby.selectMod()


# 모드변경을 strategy Pattern로 접목해보는게 좋을듯
mod = Lobby()
mod_command = ModCommand(mod, ['Intro', 'printMod', 'selectMod'])
mod_command.execute()
