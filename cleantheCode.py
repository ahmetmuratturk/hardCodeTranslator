import os
import re
from bs4 import BeautifulSoup
from htmlmin import minify

# Specify the folder path
folder_path = "ClassCentral"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        # Load the HTML file
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unnecessary tags
        for tag in soup(['header', 'nav', 'footer']):
            tag.extract()

        # Remove redundant attributes
        for tag in soup.findAll(True):
            tag.attrs = {key: val for key, val in tag.attrs.items()
                         if key in ['class', 'id', 'style']}

        # Fix broken tags
        for tag in soup.findAll(True):
            tag.unwrap()

        # Minify the HTML code
        minified_html = minify(str(soup), remove_empty_space=True, remove_comments=True)

        # Save the minified HTML code to the same file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(minified_html)
