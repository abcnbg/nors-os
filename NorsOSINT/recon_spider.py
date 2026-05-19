#!/usr/bin/env python3
# NorsOSINT - Automated Social & Infrastructure Reconnaissance
# License: GPLv3
import requests
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

# List of common social platforms
PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://nitter.net/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "HackerOne": "https://hackerone.com/{}",
}

def check_username(username, platform, url):
    target = url.format(username)
    headers = {"User-Agent": "Mozilla/5.0 NorsOSINT Scanner"}
    try:
        response = requests.get(target, headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] FOUND{Style.RESET_ALL} - {platform}: {target}")
        elif response.status_code == 404:
            pass
        else:
            print(f"{Fore.YELLOW}[?] UNKNOWN ({response.status_code}){Style.RESET_ALL} - {platform}: {target}")
    except Exception:
        print(f"{Fore.RED}[!] ERROR{Style.RESET_ALL} connecting to {platform}")

def scan_username(username):
    print(f"\n[*] Scanning for username: {Fore.CYAN}{username}{Style.RESET_ALL}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for platform, url in PLATFORMS.items():
            executor.submit(check_username, username, platform, url)

def scan_ip(ip):
    print(f"\n[*] Retrieving OSINT for IP: {Fore.CYAN}{ip}{Style.RESET_ALL}")
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json").json()
        print(f"  Organization: {res.get('org', 'N/A')}")
        print(f"  Location: {res.get('city', 'N/A')}, {res.get('region', 'N/A')}, {res.get('country', 'N/A')}")
        print(f"  Coordinates: {res.get('loc', 'N/A')}")
    except Exception as e:
        print("[-] Failed to retrieve IP data.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NorsOSINT Spider")
    parser.add_argument("-u", "--username", help="Target username to hunt")
    parser.add_argument("-i", "--ip", help="Target IP address for geolocation")
    
    args = parser.parse_args()
    print("🦅 NorsOSINT Spider Initialized")
    
    if args.username:
        scan_username(args.username)
    if args.ip:
        scan_ip(args.ip)
    
    if not args.username and not args.ip:
        parser.print_help()
