Scrape the webpage to extract all image URLs.

Download the images locally.

Generate the hashes for the downloaded images.

Step 1: Install the Required Libraries

First, install the required libraries:

pip install requests beautifulsoup4 Pillow imagehash

Step 2: Scraping the Webpage and Extracting Image URLs

Create a script that scrapes the webpage, extracts all image URLs, and downloads the images.

import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import imagehash

# Function to fetch all image URLs from a webpage
def get_image_urls(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all image tags and extract the 'src' attribute
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    
    # Ensure full URLs if the 'src' is a relative path
    img_urls = [url if url.startswith('http') else page_url + url for url in img_urls]
    
    return img_urls

# Function to download images from the URLs
def download_image(img_url, download_folder="downloaded_images"):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    img_name = img_url.split("/")[-1]
    img_path = os.path.join(download_folder, img_name)
    
    # Download the image
    img_data = requests.get(img_url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    
    return img_path

# Function to generate a hash for an image
def generate_image_hash(image_path):
    image = Image.open(image_path)
    return imagehash.average_hash(image)

# Main function to scrape, download, and hash images
def scrape_and_hash_images(page_url):
    img_urls = get_image_urls(page_url)
    print(f"Found {len(img_urls)} images.")
    
    image_hashes = {}
    
    for img_url in img_urls:
        img_path = download_image(img_url)
        img_hash = generate_image_hash(img_path)
        image_hashes[img_url] = img_hash
        
        print(f"Image: {img_url}")
        print(f"Hash: {img_hash}")
    
    return image_hashes

# Example usage
if __name__ == "__main__":
    page_url = "https://example.com"  # Replace with your target URL
    image_hashes = scrape_and_hash_images(page_url)
