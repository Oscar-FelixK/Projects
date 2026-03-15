from PIL import Image
import pyautogui as auto
import time
import pytesseract
from pynput import mouse

import mouse
from pynput import mouse

clicked = False

def on_click(x, y, button, pressed):
    global clicked
    clicked = pressed   # True when pressed, False when released

listener = mouse.Listener(on_click=on_click)
listener.start()

# Example loop
while True:
    if clicked:
        print(auto.position())
    time.sleep(1)
