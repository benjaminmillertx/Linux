Tool Name: SocialHunter
Description: A script to collect publicly available information from social media profiles and web services to help with OSINT (Open Source Intelligence) gathering for penetration testers.

(Python):

python
Copy
Edit
import requests
from bs4 import BeautifulSoup

def get_profile_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    profile_data = {
        'name': soup.find('meta', property='og:title')['content'],
        'bio': soup.find('meta', property='og:description')['content']
    }
    return profile_data

if __name__ == "__main__":
    url = input("Enter the social media profile URL: ")
    profile_info = get_profile_info(url)
    print(f"Profile Info: {profile_info}")
