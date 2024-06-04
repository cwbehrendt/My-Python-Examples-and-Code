import os
import pandas as pd
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def analyze_file(filepath, keywords):
    results = []

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        blob = TextBlob(content)

        for keyword in keywords:
            for sentence in blob.sentences:
                if keyword in sentence.words:
                    context = str(sentence)
                    context = replace_newlines_with_spaces(context)
                    if is_context_useful(context):
                        results.append((filename, keyword, context))

    return results

def replace_newlines_with_spaces(text):
    return text.replace("\n", " ")

def is_context_useful(context):
    max_non_alnum_characters = 25

    non_alnum_count = sum(1 for c in context if not c.isalnum())
    
    if len(context) < 35 or non_alnum_count > max_non_alnum_characters:
        return False
    return True

def save_to_csv(master_csv_path, results):
    with open(master_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File', 'Keyword', 'Context'])

        for file, keyword, context in results:
            writer.writerow([file, keyword, context])

def count_keywords_in_file(filepath, keywords):
    keyword_count = {keyword: 0 for keyword in keywords}

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        blob = TextBlob(content)

        for keyword in keywords:
            for sentence in blob.sentences:
                if keyword in sentence.words:
                    keyword_count[keyword] += 1

    return keyword_count

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def create_keyword_counts_summary(keyword_counts, summary_path, keywords):
    summary_df = pd.DataFrame.from_dict(keyword_counts, orient='index')
    summary_df.columns = [f'{keyword} Mentions' for keyword in keywords]
    summary_df.index.name = 'File'

    if summary_path.endswith('.csv'):
        summary_df.to_csv(summary_path)
    elif summary_path.endswith('.xlsx'):
        summary_df.to_excel(summary_path)

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title='Select a directory containing .txt files')
    return directory

if __name__ == "__main__":
    selected_directory = select_directory()
    if selected_directory:
        keywords = ['cost increase', 'commodities', 'inflation', 'deflation', 'headwinds', 'tailwinds']

        keyword_counts = defaultdict(dict)
        results = []
        sentiment_polarities = []  

        master_csv_path = os.path.join(selected_directory, 'master_analysis.csv')

        for root, _, files in os.walk(selected_directory):
            for filename in files:
                if filename.endswith('.txt'):
                    filepath = os.path.join(root, filename)
                    file_keyword_count = count_keywords_in_file(filepath, keywords)
                    keyword_counts[filename] = file_keyword_count
                    results.extend(analyze_file(filepath, keywords))
                    print(f"Keyword counts for '{filename}': {file_keyword_count}")

                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        sentiment_polarity, sentiment_subjectivity = analyze_sentiment(content)
                        sentiment_polarities.append(sentiment_polarity)  
                        print(f"Sentiment polarity for '{filename}': {sentiment_polarity}")
                        print(f"Sentiment subjectivity for '{filename}': {sentiment_subjectivity}")

                    

        
        with open(master_csv_path, 'r', encoding='utf-8') as master_csv_file:
            master_csv_reader = csv.reader(master_csv_file)
            headers = next(master_csv_reader)
            headers.extend(['Sentiment Polarity'])
            updated_rows = [headers]

            for index, row in enumerate(master_csv_reader):
                if len(row) >= 3:
                    if index < len(sentiment_polarities):
                        sentiment_polarity = sentiment_polarities[index]  
                        row.extend([sentiment_polarity])
                        updated_rows.append(row)

        with open(master_csv_path, 'w', newline='', encoding='utf-8') as master_csv_file:
            master_csv_writer = csv.writer(master_csv_file)
            master_csv_writer.writerows(updated_rows)

        keyword_summary_path = os.path.join(selected_directory, 'keyword_counts_summary.csv')
        create_keyword_counts_summary(keyword_counts, keyword_summary_path, keywords)
        save_to_csv(master_csv_path, results)

        print(f"Keyword counts summary saved to '{keyword_summary_path}'")
        print(f"Master file with context and sentiment saved to '{master_csv_path}'")


