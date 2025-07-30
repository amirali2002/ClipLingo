import pyperclip
import keyboard
import threading
import tkinter as tk
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import os


word_map = {
    "a": "ا",
    "e": "ه",
    "A": "آ",
    "b": "ب",
    "c": "س",
    "d": "د",
    "f": "ف",
    "g": "گ",
    "h": "ح",
    "i": "ی",
    "j": "ج",
    "k": "ک",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "o": "و",
    "p": "پ",
    "r": "ر",
    "s": "س",
    "t": "ت",
    "v": "و",
    "w": "و",
    "z": "ز",
    "zh": "ژ",
    "kh": "خ",
    "ch": "چ",
    "sh": "ش",
    "gh": "ق",
    "th": "ث",
    "ph": "ف",
    "ea": "ع",
    "slm": "سلام ",
    "mn": "من ",
    "hasan": "حسن",
    "mmd": "ممد",
    " ": " ",
    ",": ",",
    ".": ".",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
    "0": "۰",
    "apple":"apple",
}

is_active = True
icon = None 

def create_indicator_window():
    global indicator_window, canvas, oval
    indicator_window = tk.Tk()
    indicator_window.overrideredirect(True)
    indicator_window.attributes("-topmost", True)
    indicator_window.config(bg='white')
    indicator_window.wm_attributes("-transparentcolor", "white")
    indicator_window.geometry("50x50+20+20")

    canvas = tk.Canvas(indicator_window, width=50, height=50, bg='white', highlightthickness=0)
    canvas.pack()

    oval = canvas.create_oval(10, 10, 40, 40, fill='yellow')
    indicator_window.withdraw()

    indicator_window.mainloop()

def show_circle():
    indicator_window.deiconify()
    indicator_window.update()
    indicator_window.after(1500, lambda: indicator_window.withdraw())

def convert_text(text):
    i = 0
    result = ""
    while i < len(text):
        if i+1 < len(text):
            two_chars = text[i:i+2].lower()
            if two_chars in word_map:
                result += word_map[two_chars]
                i += 2
                continue
        char = text[i]
        mapped = word_map.get(char.lower(), char)
        result += mapped
        i += 1
    return result

def translate_clipboard():
    global is_active
    if not is_active:
        print("⛔️ برنامه غیرفعال است.")
        return
    try:
        text = pyperclip.paste()
        new_text = convert_text(text)
        if new_text != text:
            pyperclip.copy(new_text)
            print("📋 متن جدید:", new_text)
            indicator_window.after(0, show_circle)
        else:
            print("✅ نیازی به تغییر نبود.")
    except Exception as e:
        print("❌ خطا:", e)

def listen_hotkey():
    keyboard.add_hotkey('ctrl+b', translate_clipboard)
    keyboard.wait()

def toggle_text(item):
    return "خاموش" if is_active else "روشن"

def create_icon_image(color):
    image = Image.new("RGB", (64, 64), color)
    draw = ImageDraw.Draw(image)
    draw.ellipse((10,10,54,54), fill=color)
    return image

def toggle_action(icon_obj, item):
    global is_active, icon
    is_active = not is_active
    print("وضعیت:", "فعال ✅" if is_active else "غیرفعال ❌")
    new_color = (255, 255, 0) if is_active else (255, 165, 0) 
    icon.icon = create_icon_image(new_color)
    icon.update_menu()

def exit_action(icon_obj, item):
    icon_obj.stop()
    os._exit(0)

def run_tray():
    global icon
    icon = Icon("Finglish2Farsi", create_icon_image((255, 255, 0)), "مترجم فینگلیش", 
                Menu(
                    MenuItem(toggle_text, toggle_action),
                    MenuItem("خروج", exit_action)
                ))
    icon.run()

if __name__ == "__main__":
    t_circle = threading.Thread(target=create_indicator_window, daemon=True)
    t_circle.start()

    t_hotkey = threading.Thread(target=listen_hotkey, daemon=True)
    t_hotkey.start()

    run_tray()
