Tool Name: SubSniffer
Description: This tool is used to scan domains for subdomains by querying DNS servers and utilizing various public API sources to uncover hidden web infrastructure.

Legal Disclaimer: This is based on open techniques and can be used for reconnaissance within authorized testing.

Example Code Snippet (Python):

python
Copy
Edit
import requests
import dns.resolver

def find_subdomains(domain):
    subdomains = []
    dns_query = dns.resolver.Resolver()
    try:
        result = dns_query.resolve(domain, 'NS')
        for ns in result:
            subdomains.append(ns.to_text())
    except Exception as e:
        print(f"Error: {e}")
    return subdomains

if __name__ == "__main__":
    domain = input("Enter the domain to scan: ")
    subdomains = find_subdomains(domain)
    print("Subdomains found: ", subdomains)
