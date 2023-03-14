import os
from bs4 import BeautifulSoup

# Define the directory to search
directory = 'ClassCentral_Hi'

# Recursively search the directory for HTML files
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            # Read the HTML file
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find all instances of the strings you want to delete
            to_delete = soup.find_all(['!DOCTYPE', '!-- /Added by HTTrack --', 
                                       '!-- Including google analytics. The parameter ganalytics_id must be set in parameters.ini -->'])

            # Delete the strings
            for element in to_delete:
                element.extract()

            # Write the modified HTML back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
