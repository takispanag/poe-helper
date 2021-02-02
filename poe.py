from cv2 import cv2 as cv
import numpy as np
import os,sys
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
from pygtail import Pygtail

def main():
    # Change the working directory to the folder this script is in.
    # Doing this because I'll be putting the files from each video in their own folder on GitHub
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    concurrent.futures.ThreadPoolExecutor(1).submit(kill_process) #thread gia killswitch otan patisw 'x'
    
    concurrent.futures.ThreadPoolExecutor(1).submit(read_logs, "D:\Games\POE\logs\Client.txt")
    #empty_stash_after_trade()
    
    # if is_trade_window_open():
    #     count_in_trade_items()

def count_in_trade_items():
    pyautogui.moveTo(780, 520, 0.01)
    wincap = WindowCapture('Path of Exile','trade')
    # initialize the Vision class
    vision_chaos = Vision('images\chaos_bgr.jpg')
    chaos = 0
    wanted_chaos = 50
    while(chaos < wanted_chaos and is_trade_window_open()):
        chaos = 0
        # get an updated image of the game
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imwrite('images\screenshot.jpg',screenshot)
        
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
        if(chaos < wanted_chaos):
            pyautogui.moveTo(780, 520, 0.01)
            sleep(2)
    print('Done.')


def is_trade_window_open():
    focus_poe()
    window_open = pyautogui.locateOnScreen("images\/trade.jpg", confidence=.9)
    if window_open is not None:
        print("Trade window found.")
        return True
    else:
        print("Trade window wasn't found.")
        return False

def send_trade(buyer):
    focus_poe()
    trade_command = ("/tradewith {}".format(buyer))
    pyautogui.press("enter")
    pyautogui.typewrite(trade_command)
    pyautogui.press("enter")
    print("Sent trade request to: {}".format(buyer))

def send_invite(buyer):
    focus_poe()
    invite_command = ("/invite "+buyer)
    pyautogui.press("enter")
    pyautogui.typewrite(invite_command)
    pyautogui.press("enter")
    print("Invite sent to : ",buyer)


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
    print("Emptied stash.")

def kill_process():
    #If i press X the proccess and the threads are killed
    while True:
        if keyboard.is_pressed('x'):
            print("You pressed X process killed.")
            os._exit(1)
        sleep(0.3)

def focus_poe():
    #focus poe
    try:
        hwnd = win32gui.FindWindow(None, 'Path of Exile')
        win32gui.SetForegroundWindow(hwnd)
        sleep(0.3)
    except:
        print("Path of Exile not open! Please open it and run again.")
        os._exit(1)

def get_player_in_hideout(line):
    global players_in_hideout
    player_in_hideout_name = re.search('(?:.*: )(.*) has joined the area.',line)
    if player_in_hideout_name!=None :
        print("Player {} entered my hideout.".format(player_in_hideout_name[1]))
        players_in_hideout.append(player_in_hideout_name[1])
        do_trade(player_in_hideout_name[1])
        
def do_trade(player_in_hideout_name):
    global trade_tries
    while trade_tries<2:
        if player_in_hideout_name in invited_trades: #if i send invite to player and is in hideout
            send_trade(player_in_hideout_name)
            trade_tries += 1
            trade_window_open = False
            while not trade_window_open:
                trade_request_sent = pyautogui.locateOnScreen("images/trade_request.jpg", confidence=.9)
                if trade_request_sent == None and is_trade_window_open():
                    trade_window_open = True
                    count_in_trade_items()


        
def get_whisper_info(line):
    global whisper_count
    line_trade = re.search('@From(?: <"\w*">)? (\w*): Hi, I would like to buy your (.*) listed for (.*) in ',line) #item buy
    if line_trade == None:
        line_trade = re.search("""@From(?: <"\w*">)? (\w*): Hi, I'd like to buy your (.*) for my (.*) in""",line) #currency buy
    if line_trade != None:
        #take all the needed arguments from the (.*)
        #get buyer_full_name from full username and guild. Example: <"UJ"> DoTMadness I only get DoTMadness
        buyer_name = line_trade[1]
        my_currency = line_trade[2]
        their_currency = line_trade[3]
        whisper_count = whisper_count + 1
        print("---Whisper number: {}---\nBuyer: \t\t{}\nMy currency: \t{}\nFor their: \t{}\n".format(whisper_count, buyer_name, my_currency, their_currency))
        return [buyer_name, my_currency, their_currency]
        # if trade_reqs_met():
        #     send_invite(buyer_name)

def read_logs(file_name):
    try:
        os.remove("log.offset")
    except OSError:
        pass

    global currency
    global invited_trades
    while True:
        for line in Pygtail(file_name, read_from_end=True, full_lines=True, offset_file='log.offset'):
            whisper_info = get_whisper_info(line)
            if whisper_info != None:
                if(check_trade_ratios(whisper_info)):
                    send_invite(whisper_info[0])
            get_player_in_hideout(line)

def check_trade_ratios(whisper_info):
    global invited_trades
    buying_currency = re.search("\d* (\w*( \w*)?)",whisper_info[2])[1]
    buying_amount = int(re.search("(\d*) \w*",whisper_info[2])[1])
    selling_currency = re.search("\d* (\w*( \w*)?)",whisper_info[1])[1]
    selling_amount = int(re.search("(\d*) \w*",whisper_info[1])[1])
    print("buying_currency= {}, buying_amount= {}\nselling_currency= {}, selling_amount= {}".format(buying_currency,buying_amount,selling_currency,selling_amount))
    if(buying_amount <= 0 or selling_amount <= 0 ):
        print("Trade ratios bad.")
        return False
    elif(buying_amount*currency["Chromatic Orb-Chaos Orb"][0]>=selling_amount):
        print('Trade ratios ok.\nSending invite..')
        invited_trades.update({whisper_info[0]:[whisper_info[1],whisper_info[2]]})
        return True
    else:
        print("Trade ratios bad.")
        return False

if __name__ == "__main__":
    players_in_hideout = [] #global list
    invited_trades = {}
    whisper_count = 0 #global 
    trade_tries = 0
    currency = {
        "Chromatic Orb-Chaos Orb":[7,1]
    }
    main()