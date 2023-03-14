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
downloads_dir = 'downloads'
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

# download the main HTML file of the website and rename it
parsed_url = urlparse(url)
main_html_file_path = os.path.join(downloads_dir, os.path.basename(parsed_url.path))
with open(main_html_file_path, 'w') as f:
    f.write(response.text)

# download all images on the website and update their src attribute in the HTML
for img in soup.find_all('img'):
    img_url = img.get('src')
    if img_url:
        img_url = urljoin(url, img_url)
        img_response = requests.get(img_url)
        img_file_path = os.path.join(downloads_dir, os.path.basename(img_url))
        with open(img_file_path, 'wb') as f:
            f.write(img_response.content)
        img['src'] = os.path.basename(img_url)

# download all CSS files on the website and update their href attribute in the HTML
for link in soup.find_all('link', rel='stylesheet'):
    css_url = link.get('href')
    if css_url:
        css_url = urljoin(url, css_url)
        css_response = requests.get(css_url)
        css_file_path = os.path.join(downloads_dir, os.path.basename(css_url))
        with open(css_file_path, 'w') as f:
            f.write(css_response.text)
        link['href'] = os.path.basename(css_url)

# download all scripts on the website and update their src attribute in the HTML
for script in soup.find_all('script'):
    if script.get('src'):
        script_url = script.get('src')
        if script_url:
            script_url = urljoin(url, script_url)
            script_response = requests.get(script_url)
            script_file_path = os.path.join(downloads_dir, os.path.basename(script_url))
            with open(script_file_path, 'w') as f:
                f.write(script_response.text)
            script['src'] = os.path.basename(script_url)

# update all links in the HTML to point to the downloaded files
for a in soup.find_all('a'):
    href = a.get('href')
    if href:
        href = urljoin(url, href)
        if href.endswith('.html'):
            href_file_path = os.path.join(downloads_dir, os.path.basename(href))
            a['href'] = os.path.basename(href)

# save the updated HTML to the main file
with open(main_html_file_path, 'w') as f:
    f.write(str(soup))

''''
import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse

# Set the URL of the website to download
url = "https://www.classcentral.com/"

# Set the maximum depth to download
max_depth = 1

# Set the output directory for downloaded files
output_dir = "website"

# Set custom headers to avoid being blocked by robots.txt and user agent detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Set custom cookies to avoid being blocked by user session tracking
cookies = {
    'sessionid': '12345'
}

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define a function to download a page and its links
def download_page(url, depth):
    # Download the page
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code != 200:
        return

    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the page to a file
    path = url[len("http://"):]
    path = path.replace("/", "-")
    if path == "":
        path = "index"
    with open(os.path.join(output_dir, f"{path}.html"), "w") as f:
        f.write(response.text)

    # Download the links on the page up to the maximum depth
    if depth < max_depth:
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.startswith("http://") or href.startswith("https://"):
                download_page(href, depth + 1)
            else:
                url_parts = urlparse(url)
                base_url = f"{url_parts.scheme}://{url_parts.netloc}"
                link_url = urljoin(base_url, href)
                if link_url.startswith(url):
                    download_page(link_url, depth + 1)

    # Download the resources on the page
    for resource in soup.find_all(['img', 'link', 'script']):
        if resource.name == 'img':
            src = resource.get('src')
        else:
            src = resource.get('href')
        if src is None:
            continue
        if src.startswith("http://") or src.startswith("https://"):
            continue
        url_parts = urlparse(url)
        base_url = f"{url_parts.scheme}://{url_parts.netloc}"
        resource_url = urljoin(base_url, src)
        resource_path = resource_url[len(base_url):]
        resource_dir = os.path.join(output_dir, os.path.dirname(resource_path))
        if not os.path.exists(resource_dir):
            os.makedirs(resource_dir)
        with open(os.path.join(output_dir, resource_path), "wb") as f:
            response = requests.get(resource_url, headers=headers, cookies=cookies)
            if response.status_code != 200:
                continue
            f.write(response.content)

# Download the main page and its links
download_page(url, 0)
'''
