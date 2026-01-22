from PIL import Image
import pyautogui as auto
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


desired_score = int(input("What score do you want?"))
screenWidth, screenHeight = auto.size()
list_of_words = []
auto.hotkey("alt", "tab")
start_button = (1271, 586)
submit_button = (1274, 531)
next_button = (1274, 600)
text_box = (1274, 450)
auto.click(start_button)
for i in range(10):
    prompt_number = ""
    while len(prompt_number) != i + 2:
        print(len(prompt_number), prompt_number)
        auto.moveTo(screenWidth//2, screenHeight//2)
        im = auto.screenshot(region=(800, 368, 1600, 100))
        im = im.convert("L")
        im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
        im = ImageOps.invert(im)     # white number becomes black (Tesseract likes this)
        im = im.point(lambda x: 0 if x < 128 else 255, "1")
        prompt_number = pytesseract.image_to_string(im, config=config)
        if len(prompt_number) == 0:
            im.show
    auto.click(text_box)
    time.sleep(4)
    print("numebr:", prompt_number)
    auto.write(prompt_number)
    time.sleep(0.5)
    auto.press('enter')
    time.sleep(0.1)
    auto.press('enter')
    
