import re
import keyboard
from tkinter import Tk
import pyperclip
import pyautogui
from time import sleep
import os

WANTED_RED = 0
WANTED_GREEN = 2
WANTED_BLUE = 0

found = False
try:
    while True:
        if keyboard.is_pressed('w'):
            if(keyboard.is_pressed('x')):
                keyboard.release('shift')
                print("You stopped the chromatic bot.")
                os._exit(1)
            print('You Pressed w Key!')
            keyboard.press('shift')

            #check if it already has the colors we want

            clipboard = pyperclip.copy('') # empty the string
            #ctrl c
            keyboard.press_and_release('ctrl+c')
            sleep(0.03)
        
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

            if item_Red_Number >= WANTED_RED and item_Green_Number >= WANTED_GREEN and item_Blue_Number >= WANTED_BLUE:
                print("Red = {}, Green = {}, Blue = {}".format(item_Red_Number,item_Green_Number,item_Blue_Number))
                print("Etoimo")
                keyboard.release('shift')
                break

            #loop until you find colors we want
            while not found:
                if(keyboard.is_pressed('x')):
                    keyboard.release('shift')
                    print("You stopped the chromatic bot.")
                    os._exit(1)
                pyautogui.click()
                clipboard = pyperclip.copy('') # empty the string
                #ctrl c
                keyboard.press_and_release('ctrl+c')
                sleep(0.03)
            
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

                if item_Red_Number >= WANTED_RED and item_Green_Number >= WANTED_GREEN and item_Blue_Number >= WANTED_BLUE:
                    print("Red = {}, Green = {}, Blue = {}".format(item_Red_Number,item_Green_Number,item_Blue_Number))
                    print("Etoimo")
                    found = True
                    keyboard.release('shift')
                    break

                print("Red = {}, Green = {}, Blue = {}".format(item_Red_Number,item_Green_Number,item_Blue_Number))
            
            keyboard.release('shift')
            break
except Exception:
    keyboard.release('shift')
