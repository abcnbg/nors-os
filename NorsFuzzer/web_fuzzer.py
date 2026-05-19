#!/usr/bin/env python3
# NorsFuzzer - Asynchronous Web Application Fuzzer
# License: GPLv3
import asyncio
import aiohttp
import sys
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

async def fetch(session, url, word):
    target = url.replace("FUZZ", word)
    try:
        async with session.get(target, timeout=5) as response:
            if response.status not in [404, 400]:
                print(f"{Fore.GREEN}[{response.status}]{Style.RESET_ALL} {target} (Size: {len(await response.text())})")
    except Exception:
        pass

async def fuzzer(url, wordlist_path, concurrency):
    print(f"{Fore.CYAN}[*] Starting NorsFuzzer on: {url}{Style.RESET_ALL}")
    print(f"[*] Concurrency Level: {concurrency}")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Error loading wordlist: {e}")
        return

    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for word in words:
            tasks.append(fetch(session, url, word))
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)
            
    print(f"{Fore.CYAN}[*] Fuzzing complete.{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NorsFuzzer - Lightning Fast Async Web Fuzzer")
    parser.add_argument("-u", "--url", required=True, help="Target URL with FUZZ keyword (e.g. http://site.com/FUZZ)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Concurrency level")
    args = parser.parse_args()
    
    if "FUZZ" not in args.url:
        print("[-] URL must contain the 'FUZZ' keyword.")
        sys.exit(1)
        
    asyncio.run(fuzzer(args.url, args.wordlist, args.threads))
