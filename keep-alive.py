#!/bin/python3 -u 
import os
import time
import random
import pyautogui
from dotenv import load_dotenv
from python_imagesearch.imagesearch import imagesearch

load_dotenv()

while 1:
    pos = imagesearch("./login.png")
	
    if pos[0] != -1:
        print("login")
        pyautogui.moveTo(410, 350, 2, pyautogui.easeOutQuad)
        pyautogui.click()
        time.sleep(1)
        pyautogui.write(os.getenv('password'))#, interval = 0.1)
        pyautogui.hotkey('enter')
        pyautogui.moveTo(420, 380, 1, pyautogui.easeOutQuad)
        time.sleep(20)
        pyautogui.click()
		
    else:
        intv1 = random.randrange(60, 120, 1)
        time.sleep(intv1)
        intv2 = random.randrange(60, 120, 1)
        time.sleep(intv2)
        #pyautogui.moveTo(random.randrange(1100, 1130, 1), random.randrange(1005, 1055, 1), 2, pyautogui.easeOutQuad)
        pyautogui.moveTo(random.randrange(540, 565, 1), random.randrange(530, 560, 1), 2, pyautogui.easeOutQuad)
        pyautogui.click()
