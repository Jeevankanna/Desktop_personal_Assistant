import pyautogui
import os
import datetime

# Folder to save screenshots
SCREENSHOT_FOLDER = "screenshots"

# Ensure the folder exists
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

# Function to take a screenshot
def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Generate timestamp
    screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"screenshot_{timestamp}.png")

    screenshot = pyautogui.screenshot()  # Capture screenshot
    screenshot.save(screenshot_path)  # Save screenshot

    return f"Screenshot saved at: {screenshot_path}"
