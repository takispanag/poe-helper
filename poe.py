from cv2 import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
import re
import pyperclip
import keyboard
from tkinter import Tk
import win32gui
from time import sleep
import concurrent.futures

def main():
    # Change the working directory to the folder this script is in.
    # Doing this because I'll be putting the files from each video in their own folder on GitHub
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    concurrent.futures.ThreadPoolExecutor(1).submit(kill_process)

    #empty_stash_after_trade()
    if is_trade_window_open():
        count_in_trade_items()

def count_in_trade_items():
    pyautogui.moveTo(780, 520, 0.01)
    wincap = WindowCapture('Path of Exile','trade')
    # initialize the Vision class
    vision_chaos = Vision('chaos_bgr.jpg')
    chaos = 0
    while(chaos<110):
        chaos = 0
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imwrite('test.jpg',screenshot)
        
        # display the processed image
        points = vision_chaos.find(screenshot, 0.9, 'rectangles')
        for i in range(len(points)):
            pyautogui.moveTo(points[i][0]+100, points[i][1]+220) #100 pixels deksia apo tin arxi kai 220 katw apo tin arxi tis efarmogis gia to trade
            clipboard = pyperclip.copy('') # empty the string
            #ctrl c
            pyautogui.hotkey('ctrl','c')
            sleep(0.05)
            #get clipboard content
            clipboard = pyperclip.paste()
            curr_number = re.search("Stack Size: (\d+)\/\d+",clipboard).group(1)#find number of stack
            curr_name = re.search("\n(.*)\n-",clipboard).group(1) #find currency name
            chaos += int(curr_number)
        print(chaos)
        if(chaos<110):
            pyautogui.moveTo(780, 520, 0.01)
            sleep(4)
    print('Done.')


def is_trade_window_open():
    focus_poe()
    window_open = pyautogui.locateOnScreen("trade.jpg", confidence=.9)
    if window_open is not None:
        print("Trade window found.")
        return True
    else:
        print("Trade window wasn't found.")
        return False

def empty_stash_after_trade():
    wincap = WindowCapture('Path of Exile','inventory')
    # initialize the Vision class
    vision_chaos = Vision('chaos_grey.jpg')
    
    keyboard.press('ctrl')
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    cv.imwrite('test.jpg',screenshot)
    
    # display the processed image
    points = vision_chaos.find(screenshot, 0.9, 'rectangles')
    hwnd = win32gui.FindWindow(None, 'Path of Exile')
    win32gui.SetForegroundWindow(hwnd)
    for i in range(len(points)):
        pyautogui.click(points[i][0]+908, points[i][1]+627) #908 pixels deksia apo tin arxi kai 627 katw apo tin arxi tis efarmogis gia to trade
    keyboard.release('ctrl')
    print("Emptied stash from chaos.")

def kill_process():
    #If i press X the proccess and the threads are killed
    while True:
        if keyboard.is_pressed('x'):
            os._exit(1)
            print("You pressed X process killed.")
        sleep(0.3)

def focus_poe():
    #focus poe
    try:
        hwnd = win32gui.FindWindow(None, 'Path of Exile')
        win32gui.SetForegroundWindow(hwnd)
        print("Found poe and set as foreground window.")
        sleep(0.3)
    except:
        print("Path of Exile not open! Please open it and run again.")
        os._exit(1)

if __name__ == "__main__":
    main()
