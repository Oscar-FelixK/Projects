import pytesseract
from PIL import Image
import pyautogui as auto
import time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


desired_score = int(input("What score do you want?"))
screenWidth, screenHeight = auto.size()
list_of_words = []
auto.hotkey("alt", "tab")
#im.show()
location_seen_button = (screenWidth//2-100,screenHeight//4+160)
location_new_button = (screenWidth//2+100,screenHeight//4+160)

for i in range(desired_score):
    im = auto.screenshot(region=(screenWidth//3,screenHeight//4, 800, 100))
    prompt_word = pytesseract.image_to_string(im)
    if prompt_word in list_of_words:
        print("seen")
        auto.moveTo(location_seen_button)
        auto.click()
    else:
        list_of_words.append(prompt_word)
        auto.moveTo(location_new_button)
        auto.click()
print(list_of_words)
