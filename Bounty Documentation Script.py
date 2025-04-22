To create a basic bug bounty documentation script in Python, we can build a script that automates the process of reporting findings (like XSS, SQL injection, etc.). This script can generate a report with necessary details about the vulnerability discovered, such as the URL, payload, and testing results.

Here's an example of how the script can look:
Bounty Documentation Script

import requests
import time
import json

# Function to test for XSS vulnerability
def test_xss(url):
    payload = "<script>alert('XSS Test');</script>"
    response = requests.get(url, params={'search': payload})
    
    if payload in response.text:
        return True
    return False

# Function to test for SQL Injection vulnerability
def test_sql_injection(url):
    payload = "' OR 1=1 --"
    response = requests.get(url, params={'id': payload})
    
    if "SQL" in response.text or "error" in response.text:
        return True
    return False

# Function to generate a report
def generate_report(vulnerability_type, url, payload, success):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report = {
        'timestamp': timestamp,
        'vulnerability': vulnerability_type,
        'url': url,
        'payload': payload,
        'success': success,
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
    xss_success = test_xss(target_url)
    xss_report = generate_report("XSS", target_url, "<script>alert('XSS Test');</script>", xss_success)
    log_report(xss_report)

    # Test for SQL Injection vulnerability
    sql_injection_success = test_sql_injection(target_url)
    sql_injection_report = generate_report("SQL Injection", target_url, "' OR 1=1 --", sql_injection_success)
    log_report(sql_injection_report)

    print("Testing complete. Reports have been generated.")
    
if __name__ == "__main__":
    main()

Breakdown of the Script:

    Functions:

        test_xss(url): Checks for basic XSS vulnerability by injecting a script tag in the URL's search parameter.

        test_sql_injection(url): Tests for SQL injection by sending a payload like "' OR 1=1 --" and checking for SQL-related errors.

        generate_report(vulnerability_type, url, payload, success): Creates a JSON-style report with the timestamp, vulnerability type, the URL tested, the payload used, and whether the vulnerability was successful.

        log_report(report): Saves the report to a JSON file called bug_bounty_reports.json.

    Main Function:

        The script tests for both XSS and SQL injection on the target_url and logs the results using the above functions.

    Log File:

        The reports are saved in a file called bug_bounty_reports.json, and each entry is separated by a newline for easy parsing.

How to Use:

    Modify the target_url variable to point to the vulnerable web application you're testing.

    The script automatically tests for XSS and SQL injection vulnerabilities.

    Once the tests are completed, the results will be saved in a JSON file, and you can share it as your bug bounty report.

Example Output:

{
    "timestamp": "2025-04-22 14:30:12",
    "vulnerability": "XSS",
    "url": "http://example.com/vulnerable-page",
    "payload": "<script>alert('XSS Test');</script>",
    "success": true
}
{
    "timestamp": "2025-04-22 14:30:13",
    "vulnerability": "SQL Injection",
    "url": "http://example.com/vulnerable-page",
    "payload": "' OR 1=1 --",
    "success": true
}

This provides a clear, structured report that can be used for bug bounty submissions.
