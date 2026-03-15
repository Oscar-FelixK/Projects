from PIL import Image, ImageOps
import pyautogui as auto
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

screenWidth, screenHeight = auto.size()
auto.hotkey("alt", "tab")
start_button = (1268, 570)
submit_button = (1274, 531)
next_button = (1274, 600)
text_box = (1272, 431)
auto.click(start_button)
for i in range(10):
    prompt_number = ""
    #while len(prompt_number) != i + 2:
    print(len(prompt_number), prompt_number)
    im = auto.screenshot(region=(screenWidth//2-40*(i+1), 374, 80*(i+1), 100))
    im = im.convert("L")
    im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
    im = ImageOps.invert(im)     # white number becomes black (Tesseract likes this)
    im = im.point(lambda x: 0 if x < 128 else 255, "1")
    prompt_number = pytesseract.image_to_string(im, config=config)
    im.show()
    time.sleep((2*(i+1)))
    auto.click(text_box)
    print("numebr:", prompt_number)
    auto.write(prompt_number)
    time.sleep(0.5)
    auto.press('enter')
    time.sleep(0.1)
    auto.press('enter')
    
