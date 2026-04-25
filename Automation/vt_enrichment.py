import requests
import json
import sys
import os

# API key is loaded from environment variable — NEVER hardcode secrets in code!
# To set it, run in PowerShell: $env:VT_API_KEY = "your_key_here"
VT_API_KEY = os.environ.get("VT_API_KEY", "")

if not VT_API_KEY:
    print("[-] Error: VT_API_KEY environment variable not set.")
    print("    Run:  $env:VT_API_KEY = 'your_virustotal_api_key'")
    sys.exit(1)
VT_URL = "https://www.virustotal.com/api/v3/ip_addresses/"

def enrich_ip(ip_address):
    """
    Queries VirusTotal API to get the reputation score of an IP address.
    This simulates a SOAR (Security Orchestration, Automation, and Response) playbook.
    """
    print(f"[*] Starting Enrichment Playbook for IP: {ip_address}")
    
    headers = {
        "accept": "application/json",
        "x-apikey": VT_API_KEY
    }
    
    try:
        response = requests.get(VT_URL + ip_address, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant threat stats
            stats = data['data']['attributes']['last_analysis_stats']
            malicious_count = stats.get('malicious', 0)
            suspicious_count = stats.get('suspicious', 0)
            total_engines = sum(stats.values())
            
            print("\n[+] --- Enrichment Results ---")
            print(f"IP Address: {ip_address}")
            print(f"Malicious Flags: {malicious_count} / {total_engines}")
            print(f"Suspicious Flags: {suspicious_count}")
            
            # Determine Priority based on findings
            if malicious_count > 5:
                print("🚨 Priority: CRITICAL - Confirmed malicious activity!")
                print("Action: Initiate block on firewall / NSG immediately.")
            elif malicious_count > 0 or suspicious_count > 0:
                print("⚠️ Priority: HIGH - Suspicious activity detected.")
                print("Action: Escalate to SOC Analyst L2 for deeper investigation.")
            else:
                print("✅ Priority: LOW - No immediate threats found.")
                
        elif response.status_code == 401:
            print("[-] Error: Invalid API Key. Please update VT_API_KEY.")
        else:
            print(f"[-] Error querying VT: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"[-] Workflow failed: {str(e)}")

if __name__ == "__main__":
    # Test the playbook with a known malicious IP or an argument
    if len(sys.argv) > 1:
        target_ip = sys.argv[1]
    else:
        # Example IP for testing (often flagged as scanner or malicious)
        target_ip = "185.153.199.117"
        
    enrich_ip(target_ip)
