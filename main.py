import pyautogui
import time
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox

def take_screenshots(num_pages):
    screenshots = []

    # Get screen height for full-page scrolling
    screen_width, screen_height = pyautogui.size()
    
    for i in range(num_pages):
        screenshot_path = f"screenshot_{i}.png"

        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        screenshots.append(screenshot_path)

        # Scroll down by screen height
        pyautogui.scroll(-screen_height)
        time.sleep(1)  # Wait for the page to load

    return screenshots

def convert_to_pdf(screenshots, output_pdf="screenshot.pdf"):
    pdf = FPDF()

    for image_path in screenshots:
        pdf.add_page()
        pdf.image(image_path, x=0, y=0, w=210)  # A4 width

    pdf.output(output_pdf)
    messagebox.showinfo("Success", f"PDF saved as {output_pdf}")

def start_screenshot():
    try:
        num_pages = int(entry.get())
        if num_pages <= 0:
            raise ValueError("Enter a positive number")

        messagebox.showinfo("Starting", "Move to the page you want to capture. Process starts in 3 seconds.")
        time.sleep(3)  # Give time to switch to the desired window

        screenshots = take_screenshots(num_pages)
        convert_to_pdf(screenshots)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

# GUI Setup
root = tk.Tk()
root.title("Auto Screenshot to PDF")
root.geometry("300x200")

label = tk.Label(root, text="Enter number of pages:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

start_button = tk.Button(root, text="Start Screenshot", command=start_screenshot)
start_button.pack(pady=20)

root.mainloop()
