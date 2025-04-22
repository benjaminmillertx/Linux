✅ Requirements:

    Python 3.x

    PyAutoGUI

    scrot (for screenshot support on Linux)

Install everything:

sudo apt install scrot
pip install pyautogui

🧠 Full Python Script with Comments

import pyautogui
import time

# --- Screen Info ---
# Get screen width and height
screenWidth, screenHeight = pyautogui.size()
print(f"Screen resolution: {screenWidth}x{screenHeight}")

# Move mouse to center of the screen
pyautogui.moveTo(screenWidth / 2, screenHeight / 2, duration=1)

# --- Mouse Movement ---
# Move to an absolute position (100, 100)
pyautogui.moveTo(100, 100, duration=1)

# Move relative to current position (e.g., move right by 200 pixels)
pyautogui.moveRel(200, 0, duration=1)

# --- Clicks ---
# Left click at a specific location
pyautogui.click(100, 100)

# Double click
pyautogui.doubleClick(100, 100)

# Right click
pyautogui.rightClick(100, 100)

# --- Dragging ---
# Drag mouse to (100,100) over 2 seconds
pyautogui.dragTo(100, 100, duration=2)

# Drag mouse relative to current position (move right by 200 pixels)
pyautogui.dragRel(200, 0, duration=2)

# --- Scrolling ---
# Scroll up (positive number) or down (negative)
pyautogui.scroll(200)

# --- Typing ---
# Type out a string (with slight delay between each key)
pyautogui.typewrite('Hello world!', interval=0.1)

# Press Enter key
pyautogui.press('enter')

# Hold down and release keys (simulate key combinations)
pyautogui.keyDown('shift')
pyautogui.typewrite('this is uppercase')
pyautogui.keyUp('shift')

# --- Screenshot ---
# Take a screenshot and save as PNG
screenshot = pyautogui.screenshot()
screenshot.save('screenshot.png')

# --- Locate Image on Screen ---
# Looks for an image and returns coordinates if found
# NOTE: Ensure image is on screen and resolution matches
location = pyautogui.locateOnScreen('button.png')  # returns a Box object (left, top, width, height)
if location:
    print("Image found at:", location)
    center = pyautogui.locateCenterOnScreen('button.png')
    if center:
        pyautogui.moveTo(center, duration=1)
        pyautogui.click()
else:
    print("Image not found on screen.")

🛠 Common Use Cases on Linux
Task	Example
Auto-fill forms	pyautogui.typewrite("Name")
GUI Testing	Use locateOnScreen for UI element detection
Auto-click games	click() + loop
Screenshot bots	screenshot() + image recognition
⚠️ Tips for Linux

    screenshot not working? Install scrot:
    sudo apt install scrot

    Image matching fails? Use images with high contrast and avoid scaling changes.

    Mouse movement isn’t working? Some desktop environments (like Wayland) restrict control. Use X11 session if needed.
