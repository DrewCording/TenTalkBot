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
		pyautogui.moveTo(820, 670, 2, pyautogui.easeOutQuad)
		pyautogui.click()
		pyautogui.write(os.getenv('password'))
		pyautogui.hotkey('enter')
		pyautogui.moveTo(820, 690, 1, pyautogui.easeOutQuad)
		time.sleep(10)
		pyautogui.click()
		
	else:
		intv1 = random.randrange(60, 120, 1)
		time.sleep(intv1)
		intv2 = random.randrange(60, 120, 1)
		time.sleep(intv2)
		pyautogui.moveTo(1110, 1030, 2, pyautogui.easeOutQuad)
		pyautogui.click()
