import requests
import concurrent.futures

def print_banner():
    banner = """
    ╔══════════════════════════════════════════╗
    ║                DIR-SPIDER                ║
    ║             CODED BY RETR0_XD            ║
    ╚══════════════════════════════════════════╝
    """
    print(banner)

def highlight_status_code(status_code, url):
    if status_code == 200:
        return f"\033[92m[{status_code}] {url}\033[0m"  # Green color for 200 status
    return f"[{status_code}] {url}"

def check_directory(base_url, directory):
    if not base_url.endswith('/'):
        base_url += '/'
    
    url = f"{base_url}{directory.strip()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        return highlight_status_code(response.status_code, url)
    except requests.RequestException as e:
        return f"[!] Error connecting to {url}: {e}"

def brute_force_directories(base_url, wordlist):
    try:
        with open(wordlist, 'r') as file:
            directories = [line.strip() for line in file if line.strip()]
            print(f"[+] Loaded {len(directories)} directories from the wordlist.")
    except FileNotFoundError:
        print(f"[!] Wordlist file '{wordlist}' not found.")
        return

    print("\n[+] Starting directory brute-forcing\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(check_directory, base_url, directory): directory for directory in directories}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                print(result)

def main():
    print_banner()
    
    base_url = input("[ ENTER THE URL ]: ").strip()
    wordlist = input("[ ENTER THE WORDLIST FILE ]: ").strip()
    
    print(f"\n[+] URL: {base_url}")
    print(f"[+] Wordlist: {wordlist}\n")
    
    brute_force_directories(base_url, wordlist)

if __name__ == "__main__":
    main()
