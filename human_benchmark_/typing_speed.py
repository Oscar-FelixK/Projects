import pytesseract
from PIL import Image
import pyautogui as auto
import time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


screenWidth, screenHeight = auto.size()
list_of_words = []
auto.hotkey("alt", "tab")


im = auto.screenshot(region=(screenWidth//4,screenHeight//4+10, 1200, 240))
#im.show()
prompt_text = pytesseract.image_to_string(im)
prompt_text = prompt_text[1:]
for lines in prompt_text.splitlines():
    lines.replace("|", "I")
    auto.write(lines)
    auto.write(" ")

print(prompt_text.splitlines())
