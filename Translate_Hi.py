import os
from google.cloud import translate_v2 as translate
from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString

# Set up the Google Cloud Translation API client
key_path = os.path.join(os.path.dirname(__file__), 'keyfile.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
translate_client = translate.Client()



def translate_sentence(sentence, source_lang='en', target_lang='hi'):
    translation = translate_client.translate(sentence, source_language=source_lang, target_language=target_lang)
    return translation['translatedText']

# Define a function to translate all sentences in a string of HTML text


def translate_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    for tag in soup.find_all(text=True):
        if tag.parent.name not in ['style', 'script'] and not isinstance(tag.parent, Comment) and not isinstance(tag, Comment):
            tag.replace_with(translate_sentence(tag.string))
    return str(soup)

# Define a function to process a single HTML file
def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_text = f.read()

    # Extract the comments and code before the <html> tag
    soup = BeautifulSoup(html_text, 'html.parser')
    comments = []
    code = []
    for item in soup.contents:
        if isinstance(item, Comment):
            comments.append(str(item))
        elif isinstance(item, NavigableString):
            code.append(str(item))
        elif item.name == 'html':
            code.append(str(item))
    code = ''.join(code)

    # Translate the HTML inside the <html> tag
    translated_html = translate_html(str(soup.html))

    # Concatenate the translated HTML with the comments and code
    translated_html = '\n'.join(comments) + translated_html

    # Write the translated HTML back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(translated_html)
        print(f)


# Recursively process all HTML files in the "ClassCentral" folder and its subfolders
root_dir = 'ClassCentral_Hi'
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            file_path = os.path.join(dirpath, filename)
            process_html_file(file_path)


# Play a beep sound to signal that the file has been translated
import winsound
duration = 100000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)