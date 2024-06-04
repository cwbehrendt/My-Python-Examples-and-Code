import tkinter as tk
from tkinter import filedialog
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from collections import Counter
from matplotlib import font_manager
import os

#creates a word cloud from an image with inverse word mapping (puts the words on the inside of the image)

def select_xlsx():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    return file_path

def select_png():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    return file_path

def select_font():
    font_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf;*.otf")])
    return font_path

def create_word_cloud(xlsx_path, png_path, font_path):
    
    df = pd.read_excel(xlsx_path)

    
    words_counter = Counter(df.iloc[:, 0].astype(str))

    
    words_frequency = dict(words_counter)

    
    mask = np.array(Image.open(png_path))

    
    inverted_mask = np.invert(mask)

    
    wordcloud = WordCloud(width=800, height=800, background_color="white", mode='RGBA', mask=inverted_mask,
                          font_path=font_path,
                          colormap="coolwarm").generate_from_frequencies(words_frequency)

    
    plt.figure(figsize=(8, 8), facecolor='white')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)

    
    font_filename = os.path.basename(font_path)
    save_path = xlsx_path.replace('.xlsx', f'_wordcloud_{font_filename}_coolwarm.png')
    wordcloud.to_file(save_path)

    plt.show()


root = tk.Tk()
root.withdraw()


xlsx_path = select_xlsx()


png_path = select_png()


font_path = select_font()


create_word_cloud(xlsx_path, png_path, font_path)
