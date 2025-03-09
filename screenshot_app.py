import pyautogui
import os
from fpdf import FPDF
import tkinter as tk
import time
from tkinter import messagebox, simpledialog

def take_screenshots(num_pages, folder_name):
    screenshots = []
    screen_width, screen_height = pyautogui.size()

    for i in range(num_pages):
        screenshot_path = os.path.join(folder_name, f"screenshot_{i+1}.png")
        
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        screenshots.append(screenshot_path)

        # Update status in GUI
        status_label.config(text=f"Screenshot {i+1}/{num_pages} taken...", fg="blue")
        root.update()

        # Try different scrolling methods
        try:
            pyautogui.scroll(-screen_height)  # Scroll down by half the screen height
            time.sleep(1)
        except:
            print("Scroll method 1 failed, trying alternative...")
            pyautogui.press("down", presses=20, interval=0.05)  # Scroll using arrow keys
            time.sleep(1)

    return screenshots

def convert_to_pdf(screenshots, pdf_name, folder_name):
    pdf_path = os.path.join(folder_name, pdf_name + ".pdf")
    pdf = FPDF()
    
    for image_path in screenshots:
        pdf.add_page()
        pdf.image(image_path, x=0, y=0, w=210, h=297, type='PNG')  # A4 size
        
    pdf.output(pdf_path)
    messagebox.showinfo("Success", f"PDF saved as {pdf_path}")

def start_screenshot():
    try:
        num_pages = int(entry.get())
        if num_pages <= 0:
            raise ValueError("Enter a positive number")

        # Ask user for PDF name
        pdf_name = simpledialog.askstring("PDF Name", "Enter the name for the PDF file:")
        if not pdf_name:
            messagebox.showerror("Error", "PDF name cannot be empty!")
            return

        # Create folder with the same name as PDF
        folder_name = pdf_name
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        messagebox.showinfo("Starting", "Move to the page you want to capture. Process starts in 3 seconds.")
        time.sleep(3)  # Allow time to switch windows

        status_label.config(text="Taking screenshots...", fg="blue")
        root.update()

        screenshots = take_screenshots(num_pages, folder_name)
        convert_to_pdf(screenshots, pdf_name, folder_name)

        status_label.config(text=f"Process completed! {num_pages} screenshots taken.", fg="green")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

# GUI Setup
root = tk.Tk()
root.title("Auto Screenshot to PDF")
root.geometry("350x300")

label = tk.Label(root, text="Enter number of pages:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

start_button = tk.Button(root, text="Start Screenshot", command=start_screenshot)
start_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=10)

root.mainloop()
