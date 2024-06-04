import tkinter as tk
from tkinter import filedialog
import os
import pytesseract
from PIL import Image

#scrapes images for text using Tesseract

def extract_text(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print("Error:", e)
        return None


def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpeg;*.jpg")])
    if file_path:
        text = extract_text(file_path)
        if text:
            file_name = os.path.basename(file_path)
            text_file_path = os.path.splitext(file_name)[0] + ".txt"
            with open(text_file_path, "w") as f:
                f.write(text)
            print("Text extracted successfully and saved in:", text_file_path)
        else:
            print("Failed to extract text from the image.")


root = tk.Tk()
root.title("Text Extraction from Image")


browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack(pady=20)

root.mainloop()
