# From Python Primer Class - exploring requests
import requests
from bs4 import BeautifulSoup
import threading

# Global variable (for demonstration of resolution order)
GLOBAL_VERSION = "Scraper v1.0"

# Function to scrape a single URL
def scrape_page(url, verbose=False):
    """
    Scrapes the page title from a given URL.

    :param url: URL to scrape.
    :param verbose: If True, prints extra debug info.
    :return: Title of the page or "No Title Found".
    """
    # Debug print statement
    print("Inside scrape_page function...")
    
    # Enclosing scope variable
    local_info = "Scraping local info..."

    def show_info():
        # Access 'local_info' from enclosing scope
        print("Enclosing info:", local_info)
        # Access 'GLOBAL_VERSION' from global scope
        print("Global version:", GLOBAL_VERSION)

    # Show how we can reference different scopes
    show_info()

    # Fetch page
    response = requests.get(url)

    print("Response requests finished. Extracting title...")

    # Lambda function to extract title text
    extract_title = lambda soup_obj: soup_obj.title.string if soup_obj.title else "No Title Found"

    soup = BeautifulSoup(response.text, "html.parser")
    page_title = extract_title(soup)

    if verbose:
        print(f"Fetched {url} -> {page_title}")

    return page_title

# Wrapper function to update the results list
def update_results(index, url, results, verbose):
    results[index] = scrape_page(url, verbose=verbose)

def run_scraper():
    """
    Creates threads to scrape 3 URLs in parallel.
    """

    # Our three sample URLs (feel free to replace them with any other public pages)
    urls = [
        "https://www.python.org/downloads/release/python-31016",
        "https://techcrunch.com/2025/02/15/openai-teases-a-simplified-gpt-5-model/",
        "https://daily.dev/blog/python-and-javascript-choosing-your-first-language"
    ]

    results = [None, None, None]
    threads = []

    # Create a thread for each URL
    for i, link in enumerate(urls):
        # 'target' is the function the thread will run
        # 'args' is a tuple with the arguments for that function
        t = threading.Thread(target=update_results, args=(i, link, results, True))
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Print the final results
    for i, link in enumerate(urls):
        print(f"Title for {link}: {results[i]}")

# Actual script entry point
if __name__ == "__main__":
    # Running the scraper
    run_scraper