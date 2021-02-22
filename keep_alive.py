import os
import time
import random
import pyautogui

while 1:
	intv1 = random.randrange(60, 120, 1)
	time.sleep(intv1)
	intv2 = random.randrange(60, 120, 1)
	time.sleep(intv2)
	print("sleep time was " + str(intv1) + " + " + str(intv2))
	pyautogui.click()
