import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin

# specify the URL of the website to scrape
url = "https://example.com"

# make a GET request to the website
response = requests.get(url)

# parse the HTML content of the website using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# create a directory to store downloaded files
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# download the main HTML file of the website and rename it
parsed_url = urlparse(url)
main_html_file_path = os.path.join('downloads', os.path.basename(parsed_url.path))
with open(main_html_file_path, 'w') as f:
    f.write(response.text)

# download all images on the website and update their src attribute in the HTML
for img in soup.find_all('img'):
    img_url = img.get('src')
    if img_url:
        img_url = urljoin(url, img_url)
        img_response = requests.get(img_url)
        img_file_path = os.path.join('downloads', os.path.basename(img_url))
        with open(img_file_path, 'wb') as f:
            f.write(img_response.content)
        img['src'] = os.path.basename(img_url)

# download all CSS files on the website and update their href attribute in the HTML
for link in soup.find_all('link', rel='stylesheet'):
    css_url = link.get('href')
    if css_url:
        css_url = urljoin(url, css_url)
        css_response = requests.get(css_url)
        css_file_path = os.path.join('downloads', os.path.basename(css_url))
        with open(css_file_path, 'w') as f:
            f.write(css_response.text)
        link['href'] = os.path.basename(css_url)

# download all scripts on the website and update their src attribute in the HTML
for script in soup.find_all('script'):
    if script.get('src'):
        script_url = script.get('src')
        if script_url:
            script_url = urljoin(url, script_url
