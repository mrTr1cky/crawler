import sys

# Function to save URL to file and remove duplicates
def save_url(url):
    with open('urls.txt', 'a+') as file:
        file.seek(0)
        urls = file.readlines()
        if url + '\n' not in urls:
            file.write(url + '\n')
            print(f"Saved URL: {url}")
        else:
            print(f"URL already exists: {url}")

# Extract URL parameter passed from main_crawler.py
url_to_save = sys.argv[1]

# Call the save_url function with the URL parameter
save_url(url_to_save)
