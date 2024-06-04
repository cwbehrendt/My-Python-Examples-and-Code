import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog

def scrape_and_save(url, save_dir):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(2)  

    transcript_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/earnings/transcripts/')]")
    
    for link in transcript_links:
        href = link.get_attribute("href")
        link.click()
        time.sleep(2)
        
        transcript_text = driver.find_element(By.CLASS_NAME, "transcript-discussion").text
        page_title = driver.find_element(By.CLASS_NAME, "PageTitleHOne").text
        
        file_name = f"{page_title}.txt"
        file_path = os.path.join(save_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(transcript_text)
        
        driver.back()
        time.sleep(2)
    
    driver.quit()

def choose_directory():
    directory = filedialog.askdirectory()
    save_directory_var.set(directory)

def scrape_button_click():
    url = "https://www.marketbeat.com/earnings/transcripts/"
    save_dir = save_directory_var.get()
    scrape_and_save(url, save_dir)


root = tk.Tk()
root.title("Transcript Scraper")

save_directory_var = tk.StringVar()


label = tk.Label(root, text="Choose save directory:")
label.pack()

choose_dir_button = tk.Button(root, text="Choose Directory", command=choose_directory)
choose_dir_button.pack()

scrape_button = tk.Button(root, text="Scrape Transcripts", command=scrape_button_click)
scrape_button.pack()

root.mainloop()
