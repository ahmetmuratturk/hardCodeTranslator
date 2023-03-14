import os
from google.cloud import translate_v2 as translate

# set up the Google Translate client
key_path = os.path.join(os.path.dirname(__file__), 'keyfile.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
translate_client = translate.Client()

# function to recursively find all HTM files in the given directory
def find_htm_files(directory):
    htm_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.HTM'):
                htm_files.append(os.path.join(dirpath, filename))
    return htm_files

# function to translate a given sentence from English to Turkish
def translate_sentence(sentence):
    translation = translate_client.translate(
        sentence, target_language='tr', source_language='en')
    return translation['translatedText']

# function to process an HTM file, replacing English sentences with their Turkish translations
# function to process an HTM file, replacing English sentences with their Turkish translations
def process_htm_file(htm_file):
    with open(htm_file, 'r', encoding='utf-8') as f:
        content = f.read()
    translated_content = ''
    last_index = 0
    while True:
        start_index = content.find('>', last_index)
        if start_index == -1:
            translated_content += content[last_index:]
            break
        translated_content += content[last_index:start_index+1]
        end_index = content.find('<', start_index+1)
        if end_index == -1:
            translated_content += content[start_index+1:]
            break
        sentence = content[start_index+1:end_index]
        if not any(tag in sentence.lower() for tag in ['<html', '<head', '<title', '<script', '<style']):
            chunk_size = 500  # set the chunk size to 500 characters
            sentence_chunks = [sentence[i:i+chunk_size] for i in range(0, len(sentence), chunk_size)]
            translated_chunks = [translate_sentence(chunk) for chunk in sentence_chunks]
            translated_sentence = ''.join(translated_chunks)
            translated_content += translated_sentence
        else:
            translated_content += sentence
        last_index = end_index
    with open(htm_file, 'w', encoding='utf-8') as f:
        f.write(translated_content)


# find all HTM files in the ClassCentral folder and its subfolders
htm_files = find_htm_files('ClassCentral')

# process each HTM file, replacing English sentences with their Turkish translations
for htm_file in htm_files:
    process_htm_file(htm_file)
