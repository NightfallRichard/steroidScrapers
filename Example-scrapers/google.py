import requests
from bs4 import BeautifulSoup
import re
import time
import random

# Set a common desktop User-Agent to mimic a real browser.
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/110.0.0.0 Safari/537.36")
}

def google_search_emails(query: str, num_pages: int = 1) -> list[str]:
    """
    Perform a Google search for the provided query and extract email addresses
    from the returned HTML content.
    """
    found_emails = set()

    for page in range(num_pages):
        # Construct URL for Google search with pagination (10 results per page)
        url = f"https://www.google.com/search?q={query}&start={page*10}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract all text content from the page
            text_content = soup.get_text(separator=" ")
            # Regex to find email-like patterns
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text_content)
            found_emails.update(emails)
            # Random delay to mimic human behavior
            time.sleep(random.uniform(2, 5))
        else:
            print("Error fetching page:", response.status_code)
    
    return list(found_emails)

if __name__ == "__main__":
    # Example query that looks for emails (quotes force literal search for '@gmail.com')
    query = '"@gmail.com"'
    emails = google_search_emails(query, num_pages=2)
    print("Emails found:", emails)

