import requests
from urllib.parse import urljoin
import subprocess
import concurrent.futures

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

# Function to crawl URLs
def crawl_url(url, visited, max_depth, current_depth):
    if current_depth > max_depth or url in visited:
        return

    try:
        response = requests.get(url)
        status_code = response.status_code
        visited.add(url)

        if status_code in [200, 403]:
            print(f"{GREEN}[ Crawling... ]{ENDC} {url}")

            found_links = False
            for link in response.text.split('href="')[1:]:
                href = link.split('"', 1)[0]
                if href.startswith(base_url):
                    new_url = urljoin(base_url, href)
                    if new_url not in visited:
                        found_links = True
                        crawl_url(new_url, visited, max_depth, current_depth + 1)

            subprocess.run(["python", "url_manager.py", url])

            if not found_links:
                print(f"{RED}[ No links found ]{ENDC} {url}")

        elif status_code == 403:
            print(f"{RED}[ Forbidden: {status_code} ]{ENDC} {url}")
        else:
            print(f"{RED}[ Failed: {status_code} ]{ENDC} {url}")

    except Exception as e:
        print(f"{RED}[ Error: {e} ]{ENDC} {url}")

# Ask user for the domain name
domain_name = input("Enter Domain name: ").strip()
if not domain_name.startswith("http"):
    domain_name = "https://" + domain_name

base_url = domain_name
visited_urls = set()

# Set the maximum depth for crawling
max_depth = 3

# Define the number of threads (50 threads)
num_threads = 50

# Create a ThreadPoolExecutor with a maximum of 'num_threads' threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    # Start crawling with initial URL
    executor.submit(crawl_url, base_url, visited_urls, max_depth, current_depth=1)

