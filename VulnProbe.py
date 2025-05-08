Tool Name: VulnProbe
Description: A basic vulnerability scanner for web applications that detects common vulnerabilities like XSS (Cross-Site Scripting) and SQL injection using heuristic checks.

 (Python):

python
Copy
Edit
import requests

def check_xss(url):
    payload = "<script>alert('XSS')</script>"
    response = requests.get(url, params={'input': payload})
    if payload in response.text:
        return True
    return False

def check_sql_injection(url):
    payload = "' OR 1=1 --"
    response = requests.get(url, params={'input': payload})
    if "error" in response.text:
        return True
    return False

if __name__ == "__main__":
    url = input("Enter the web app URL to scan: ")
    if check_xss(url):
        print("XSS vulnerability detected!")
    if check_sql_injection(url):
        print("SQL Injection vulnerability detected!")
