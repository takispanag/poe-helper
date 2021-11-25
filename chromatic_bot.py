import re
import keyboard
from tkinter import Tk
import pyperclip
import pyautogui
from time import sleep
import os


# WANTED_RED = 1
# WANTED_GREEN = 0
# WANTED_BLUE = 2

print("WELCOME TO THE CHROMATIC BOT")
while True:
    try:
        WANTED_RED = int(input("How many red sockets do you want?\t"))
        WANTED_GREEN = int(input("How many green sockets do you want?\t"))
        WANTED_BLUE = int(input("How many blue sockets do you want?\t"))
        print("Please left click on a chromatic orb, hover over the item you want to change and press W")
        break
    except ValueError:
        print("Please enter a valid number.")


found = False
try:
    while True:
        if keyboard.is_pressed('w'):
            if(keyboard.is_pressed('x')):
                keyboard.release('shift')
                print("You stopped the chromatic bot.")
                os._exit(1)
            print('You Pressed w Key! Please dont move the mouse.')
            keyboard.press('shift')

            #check if it already has the colors we want

            clipboard = pyperclip.copy('') # empty the string
            #ctrl c
            keyboard.press_and_release('ctrl+c')
            sleep(0.03)
        
            #get clipboard content
            clipboard = pyperclip.paste()

            item_Red_Sockets = 0
            item_Green_Sockets = 0
            item_Blue_Sockets = 0
            r = re.findall("(R|G|B)(-| )",clipboard)
            #find R, G, B count using regex
            for i in range(0,len(r)):

                if r[i][0].strip() == "R":
                    item_Red_Sockets += 1 
                elif r[i][0].strip() == "G":
                    item_Green_Sockets += 1
                elif r[i][0].strip() == "B":
                    item_Blue_Sockets += 1

            #sockets already ready, exit program
            if item_Red_Sockets >= WANTED_RED and item_Green_Sockets >= WANTED_GREEN and item_Blue_Sockets >= WANTED_BLUE:
                print("Red = {}, Green = {}, Blue = {}".format(item_Red_Sockets,item_Green_Sockets,item_Blue_Sockets))
                print("Item ready!")
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

                item_Red_Sockets = 0
                item_Green_Sockets = 0
                item_Blue_Sockets = 0
                r = re.findall("(R|G|B)(-| ){1,6}",clipboard)
                #find R, G, B count using regex
                for i in range(0,len(r)):
                    if r[i][0].strip() == "R":
                        item_Red_Sockets += 1 
                    elif r[i][0].strip() == "G":
                        item_Green_Sockets += 1
                    elif r[i][0].strip() == "B":
                        item_Blue_Sockets += 1

                #found and stop program
                if item_Red_Sockets >= WANTED_RED and item_Green_Sockets >= WANTED_GREEN and item_Blue_Sockets >= WANTED_BLUE:
                    print("Ready! Red = {}, Green = {}, Blue = {}".format(item_Red_Sockets,item_Green_Sockets,item_Blue_Sockets))
                    found = True
                    keyboard.release('shift')
                    break

                print("Red = {}, Green = {}, Blue = {}".format(item_Red_Sockets,item_Green_Sockets,item_Blue_Sockets))
            
            keyboard.release('shift')
            break
except Exception:
    keyboard.release('shift')
