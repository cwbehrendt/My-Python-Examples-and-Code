import os
import tkinter as tk
from tkinter import filedialog
import spacy
import PyPDF2

nlp = spacy.load("en_core_web_sm")


target_keywords = ["keyword1", "keyword2", "keyword3"]

def analyze_text(text):
    doc = nlp(text)
    extracted_keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    context = doc.text

    found_keywords = [keyword for keyword in target_keywords if keyword in extracted_keywords]

    return found_keywords, context

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

def convert_pdf_to_text(pdf_path, text_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_text = extract_text_from_pdf(pdf_file)

        keywords, context = analyze_text(pdf_text)
        
        
        with open(text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(pdf_text)

        return keywords, context

    except Exception as e:
        print(f"An error occurred: {e}")
        return [], ""

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(root, filename)
                text_path = os.path.join(root, filename.replace(".pdf", ".txt"))
                keywords, context = convert_pdf_to_text(pdf_path, text_path)
                
                

def select_directory_and_convert():
    root = tk.Tk()
    root.withdraw()  
    directory_path = filedialog.askdirectory(title="Select a directory with PDF files")
    if not directory_path:
        print("No directory selected.")
        return
    process_directory(directory_path)
    print("Conversion and analysis complete.")

if __name__ == "__main__":
    select_directory_and_convert()
