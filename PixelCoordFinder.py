# Created by GiveUsername; aka nspe
# Todo: None
# Description:
    # // Allows you to find pixel coordinates on a screen and the designated pixels color. Terminal output will be the pixel above your mouse cursor. \\

import pyautogui
from PIL import ImageGrab

def get_pixel_color_above_cursor():
    x, y = pyautogui.position()
    
    screenshot = ImageGrab.grab()
    
    if 0 <= x < screenshot.width and 0 <= y < screenshot.height:
        # Retrieve the pixel color at the cursor position
        pixel_color = screenshot.getpixel((x, y))
        return pixel_color
    else:
        return None

if __name__ == "__main__":
    try:
        while True:
            pixel_color = get_pixel_color_above_cursor()
            if pixel_color:
                print(f"Pixel color at ({pyautogui.position()}): {pixel_color}")
    except KeyboardInterrupt:
        print("\nExiting...")
