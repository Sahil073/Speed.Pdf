from flask import Flask, render_template, request, jsonify, send_file
import os
import pyautogui
import time
from fpdf import FPDF
from docx import Document

app = Flask(__name__)

# Directory to store screenshots and documents
SAVE_FOLDER = "saved_files"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Function to take screenshots
def take_screenshots(num_pages, folder):
    screenshots = []
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i in range(num_pages):
        screenshot_path = os.path.join(folder, f"screenshot_{i+1}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        screenshots.append(screenshot_path)
        pyautogui.scroll(-500)  # Scroll down to capture more content
        time.sleep(1)  # Small delay between screenshots

    return screenshots

# Convert screenshots to PDF
def convert_to_pdf(screenshots, pdf_name, folder):
    pdf_path = os.path.join(folder, pdf_name + ".pdf")
    pdf = FPDF()
    
    for img in screenshots:
        pdf.add_page()
        pdf.image(img, x=0, y=0, w=210, h=297)  # A4 size
    
    pdf.output(pdf_path)
    return pdf_path

# Convert screenshots to Word Document
def convert_to_word(screenshots, doc_name, folder):
    doc_path = os.path.join(folder, doc_name + ".docx")
    doc = Document()
    
    for img in screenshots:
        doc.add_paragraph(f"Image: {img}")
    
    doc.save(doc_path)
    return doc_path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capture")
def capture_screenshot():
    try:
        num_pages = int(request.args.get("pages", 1))
        pdf_name = request.args.get("name", "screenshot")

        user_folder = os.path.join(SAVE_FOLDER, pdf_name)
        screenshots = take_screenshots(num_pages, user_folder)

        pdf_path = convert_to_pdf(screenshots, pdf_name, user_folder)
        doc_path = convert_to_word(screenshots, pdf_name, user_folder)

        return jsonify({
            "message": "Screenshots captured successfully!",
            "pdf_path": pdf_path,
            "doc_path": doc_path
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/download/pdf")
def download_pdf():
    pdf_name = request.args.get("name", "screenshot")
    file_path = os.path.join(SAVE_FOLDER, pdf_name, pdf_name + ".pdf")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

@app.route("/download/word")
def download_word():
    pdf_name = request.args.get("name", "screenshot")
    file_path = os.path.join(SAVE_FOLDER, pdf_name, pdf_name + ".docx")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
