✅  Ensure DVWA Security Level is Low

DVWA must be set to "Low" security in its settings. Otherwise, many automated scanners will fail.

Go to:

http://10.0.2.13/dvwa/security.php

Set security to Low.


Here’s a fully working scanner example that you can build on:
main.py

import scanner

target_url = "http://10.0.2.13/dvwa/"
links_to_ignore = ["http://10.0.2.13/dvwa/logout.php"]
data_dict = {"username": "admin", "password": "password", "Login": "Login"}

vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
response = vuln_scanner.session.post("http://10.0.2.13/dvwa/login.php", data=data_dict)

if "Logout" in response.text:
    print("[+] Logged in successfully.")
    vuln_scanner.crawl()
    vuln_scanner.run_scanner()
else:
    print("[-] Login failed. Check your credentials or security level.")

    ------------------------------------------------------------------------------------------------------------
    2.0 DVWAscanner.py
 import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self, url, ignore_links):
        self.session = requests.Session()
        self.target_url = url
        self.links_to_ignore = ignore_links
        self.target_links = []

    def extract_links_from(self, url):
        response = self.session.get(url)
        return re.findall('(?:href=")(.*?)"', response.text)

    def crawl(self, url=None):
        if url is None:
            url = self.target_url
        href_links = self.extract_links_from(url)
        for link in href_links:
            link = urljoin(url, link)
            if "#" in link:
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                self.target_links.append(link)
                print("[+] Discovered URL --> " + link)
                self.crawl(link)

    def extract_forms(self, url):
        response = self.session.get(url)
        parsed_html = BeautifulSoup(response.text, "html.parser")
        return parsed_html.find_all("form")

    def submit_form(self, form, value, url):
        action = form.get("action")
        post_url = urljoin(url, action)
        method = form.get("method")

        inputs = form.find_all("input")
        data = {}

        for input in inputs:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value
            data[input_name] = input_value

        if method == "post":
            return self.session.post(post_url, data=data)
        return self.session.get(post_url, params=data)

    def run_scanner(self):
        for link in self.target_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n[+] Testing form on " + link)
                is_vulnerable_to_xss = self.test_xss_in_form(form, link)
                if is_vulnerable_to_xss:
                    print("\n\n[!!!] XSS vulnerability discovered in form on: " + link)
                    break

            if "=" in link:
                print("\n[+] Testing URL " + link)
                is_vulnerable_to_xss = self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print("\n\n[!!!] XSS vulnerability discovered in link: " + link)

    def test_xss_in_link(self, url):
        xss_test_script = "<script>alert('XSS')</script>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.text

    def test_xss_in_form(self, form, url):
        xss_test_script = "<script>alert('XSS')</script>"
        response = self.submit_form(form, xss_test_script, url)
        return xss_test_script in response.text   
