import os
import csv
from textblob import TextBlob


input_folder = r"FILEPATH REDACTED CAUSE COMPANY INFORMATION WAS HERE, ENJOY THIS MESSAGE"


output_csv = os.path.join(input_folder, "output.csv")


csv_file = open(output_csv, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Filename', 'Line', 'Sentiment Polarity'])


positive_threshold = 0.3
negative_threshold = -0.3


for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_folder, filename)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as txt_file:
            lines = txt_file.readlines()
            for line in lines:
                blob = TextBlob(line)
                sentiment_polarity = blob.sentiment.polarity
                if sentiment_polarity > positive_threshold or sentiment_polarity < negative_threshold:
                    csv_writer.writerow([filename, line.strip(), sentiment_polarity])


csv_file.close()

print("NLP processing and CSV creation complete.")
