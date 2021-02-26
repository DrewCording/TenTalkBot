#!/bin/python3 -u
import os
import time
import random
import pyautogui
from dotenv import load_dotenv
from python_imagesearch.imagesearch import imagesearch

while 1:
	time.sleep(0.5)
	print(pyautogui.position())