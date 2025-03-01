import asyncio
import json
import os

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel
from playwright.async_api import async_playwright

# URL for job listings on Seek (adjust as needed)
URL_TO_SCRAPE = "https://www.seek.com.au/software-developer-jobs"

# Instruction for the LLM extraction
INSTRUCTION_TO_LLM = """
Extract job title, company name, location, salary, job type, posted date, job link, 
job description, and job requirements into JSON format.
"""

# Expanded JobListing schema for more detailed extraction
class JobListing(BaseModel):
    title: str
    company: str
    location: str
    salary: str | None  # Some listings may not show salaries
    job_type: str | None  # Full-time, Part-time, Contract, etc.
    posted_date: str | None  # Posting date or how long ago it was posted
    job_link: str  # Direct link to the job listing
    description: str
    requirements: str | None  # Required skills or experience

# Example proxy config using a rotating proxy (update with your credentials)
proxy_config = {
    "server": "http://brd.superproxy.io:22225",  # e.g., BrightData rotating proxy
    "username": "your_username",
    "password": "your_password",
}

async def browse_like_human(url: str, max_pages: int = 5) -> list[str]:
    """
    Uses Playwright to load the page, scroll down to load dynamic content,
    and click the "Next" button to scrape multiple pages.
    Returns a list of HTML content for each page.
    """
    pages_html = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=False for debugging
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        
        for _ in range(max_pages):
            # Scroll down to load dynamic content
            for _ in range(3):
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                await asyncio.sleep(2)
            
            # Save the current page's HTML content
            pages_html.append(await page.content())
            
            # Try to locate and click the "Next" button for pagination
            next_button = await page.query_selector('a[data-automation="pagination-next"]')
            if next_button:
                await next_button.click()
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(3)  # Extra delay to mimic human behavior
            else:
                break  # No further pages available
        
        await browser.close()
    return pages_html

async def main():
    # Get HTML content for multiple pages
    pages_html = await browse_like_human(URL_TO_SCRAPE, max_pages=5)
    
    # Configure the LLM-based extraction strategy with the updated schema using Google Gemini
    llm_strategy = LLMExtractionStrategy(
        provider="google/gemini",
        api_key=os.environ["GOOGLE_GEMINI_API_KEY"],
        schema=JobListing.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION_TO_LLM,
        chunk_token_threshold=1000,
        apply_chunking=True,
        input_format="html",  # Since we're processing rendered HTML
        extra_args={"temperature": 0.0, "max_tokens": 1000},
    )
    
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
    )
    
    browser_cfg = BrowserConfig(proxy_config=proxy_config)
    
    all_extracted_jobs = []
    
    # Use Crawl4AI to process each page's HTML and extract job details
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        for page_html in pages_html:
            result = await crawler.arun(content=page_html, config=crawl_config)
            if result.success:
                extracted_data = json.loads(result.extracted_content)
                all_extracted_jobs.extend(extracted_data)
            else:
                print("Error on page:", result.error_message)
    
    # Save the aggregated job listings to a JSON file
    with open("seek_jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_extracted_jobs, f, indent=4)
    
    print("Extracted jobs saved to seek_jobs.json")

if __name__ == "__main__":
    asyncio.run(main())

