import re
import keyboard
from tkinter import Tk
import pyperclip
import pyautogui
from time import sleep

wanted_Red = 1
wanted_Green = 1
wanted_Blue = 0

found = False
while True:
    if keyboard.is_pressed('w'):
        print('You Pressed w Key!')
        keyboard.press('shift')

        #check if it already has the colors we want

        clipboard = pyperclip.copy('') # empty the string
        #ctrl c
        keyboard.press_and_release('ctrl+c')
        sleep(0.1)
    
        #get clipboard content
        clipboard = pyperclip.paste()

        item_Red_Number = 0
        item_Green_Number = 0
        item_Blue_Number = 0
        r = re.findall("(R|G|B)(-| ){1,6}",clipboard)
        for i in range(0,len(r)):
            if r[i][0].strip() == "R":
                item_Red_Number += 1 
            elif r[i][0].strip() == "G":
                item_Green_Number += 1
            elif r[i][0].strip() == "B":
                item_Blue_Number += 1

        if item_Red_Number >= wanted_Red and item_Green_Number >= wanted_Green and item_Blue_Number >= wanted_Blue:
            print("Red = {}, Green = {}, Blue = {}".format(item_Red_Number,item_Green_Number,item_Blue_Number))
            print("Etoimo")
            break

        #loop until you find colors we want
        while not found:
            pyautogui.click()
            clipboard = pyperclip.copy('') # empty the string
            #ctrl c
            keyboard.press_and_release('ctrl+c')
            sleep(0.1)
        
            #get clipboard content
            clipboard = pyperclip.paste()

            item_Red_Number = 0
            item_Green_Number = 0
            item_Blue_Number = 0
            r = re.findall("(R|G|B)(-| ){1,6}",clipboard)
            for i in range(0,len(r)):
                if r[i][0].strip() == "R":
                    item_Red_Number += 1 
                elif r[i][0].strip() == "G":
                    item_Green_Number += 1
                elif r[i][0].strip() == "B":
                    item_Blue_Number += 1

            if item_Red_Number >= wanted_Red and item_Green_Number >= wanted_Green and item_Blue_Number >= wanted_Blue:
                print("Red = {}, Green = {}, Blue = {}".format(item_Red_Number,item_Green_Number,item_Blue_Number))
                print("Etoimo")
                found = True
                break

            print("Red = {}, Green = {}, Blue = {}".format(item_Red_Number,item_Green_Number,item_Blue_Number))
        break