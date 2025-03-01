import asyncio
import re
import os
import json
from playwright.async_api import async_playwright

# DISCLAIMER: Ensure you comply with LinkedIn's Terms of Service and applicable laws.
# This code is for educational purposes only.

async def login_linkedin(page):
    """
    Logs in to LinkedIn using credentials stored in environment variables.
    Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your environment.
    """
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    if not email or not password:
        raise Exception("Please set the LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
    
    await page.goto("https://www.linkedin.com/login", timeout=60000)
    await page.fill("input#username", email)
    await page.fill("input#password", password)
    await page.click("button[type='submit']")
    await page.wait_for_load_state("networkidle")
    print("Logged in to LinkedIn.")

def extract_emails(html_content: str) -> list[str]:
    """
    Extracts email addresses from the provided HTML content using a regex pattern.
    """
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return re.findall(email_pattern, html_content)

async def scrape_profile_emails(profile_url: str) -> list[str]:
    """
    Navigates to a LinkedIn profile URL, retrieves the page content, and extracts email addresses.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Change to headless=False for debugging.
        page = await browser.new_page()
        
        # Log in to LinkedIn
        await login_linkedin(page)
        
        # Navigate to the public profile URL
        await page.goto(profile_url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)  # Allow time for content to load
        
        html_content = await page.content()
        emails = extract_emails(html_content)
        await browser.close()
        return list(set(emails))  # Return unique email addresses

async def main():
    # List of LinkedIn public profile URLs to scrape emails from
    profile_urls = [
        "https://www.linkedin.com/in/sample-profile1/",
        "https://www.linkedin.com/in/sample-profile2/",
        # Add additional public profile URLs as needed
    ]
    
    scraped_data = {}
    for url in profile_urls:
        try:
            emails = await scrape_profile_emails(url)
            scraped_data[url] = emails
            print(f"Profile: {url} - Emails found: {emails}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    # Save results to a JSON file
    with open("linkedin_profile_emails.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4)
    
    print("Scraping complete. Data saved to linkedin_profile_emails.json.")

if __name__ == "__main__":
    asyncio.run(main())

