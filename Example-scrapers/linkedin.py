import asyncio
import json
import os
from pydantic import BaseModel

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from playwright.async_api import async_playwright

# LinkedIn jobs URL (modify keywords as needed)
URL_TO_SCRAPE = "https://www.linkedin.com/jobs/search/?keywords=software%20developer"

# Instruction for LLM extraction
INSTRUCTION_TO_LLM = """
Extract the LinkedIn job details including title, company name, location, job link, 
job description, and posted date. Return the output in valid JSON format.
"""

# Expanded schema for LinkedIn job listings
class LinkedInJobListing(BaseModel):
    title: str
    company: str
    location: str
    job_link: str
    description: str | None
    posted_date: str | None

# Optional proxy configuration (update with your credentials or leave empty)
proxy_config = {
    "server": os.getenv("PROXY_SERVER", ""),  
    "username": os.getenv("PROXY_USERNAME", ""),
    "password": os.getenv("PROXY_PASSWORD", ""),
}

async def login_linkedin(page):
    """
    Logs in to LinkedIn using credentials provided in environment variables.
    Set the environment variables LINKEDIN_EMAIL and LINKEDIN_PASSWORD beforehand.
    """
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    if not email or not password:
        raise Exception("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
    
    await page.goto("https://www.linkedin.com/login", timeout=60000)
    await page.fill("input#username", email)
    await page.fill("input#password", password)
    await page.click("button[type='submit']")
    await page.wait_for_load_state("networkidle")

async def scrape_linkedin_jobs(url: str, max_scroll: int = 5) -> list[str]:
    """
    Uses Playwright to login to LinkedIn, navigate to the jobs page, and perform
    repeated scrolling to load dynamic content. Returns a list of HTML snapshots.
    """
    pages_html = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=False for debugging
        page = await browser.new_page()
        
        # Log in to LinkedIn first
        await login_linkedin(page)
        
        # Navigate to the LinkedIn Jobs search page
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")
        
        # Simulate scrolling to load more job listings
        for _ in range(max_scroll):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(3)  # Delay to allow new content to load
            pages_html.append(await page.content())
        
        await browser.close()
    return pages_html

async def main():
    # Retrieve HTML snapshots from multiple scrolls on the jobs page
    pages_html = await scrape_linkedin_jobs(URL_TO_SCRAPE, max_scroll=5)
    
    # Configure the LLM extraction strategy using our LinkedInJobListing schema
    llm_strategy = LLMExtractionStrategy(
        provider="ollama/deepseek-r1:14b",
        schema=LinkedInJobListing.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION_TO_LLM,
        chunk_token_threshold=1000,
        apply_chunking=True,
        input_format="html",
        extra_args={"temperature": 0.0, "max_tokens": 1000},
    )
    
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
    )
    
    browser_cfg = BrowserConfig(proxy_config=proxy_config)
    
    all_extracted_jobs = []
    
    # Use Crawl4AI to extract job details from each page's HTML snapshot
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        for page_html in pages_html:
            result = await crawler.arun(content=page_html, config=crawl_config)
            if result.success:
                extracted_data = json.loads(result.extracted_content)
                all_extracted_jobs.extend(extracted_data)
            else:
                print("Error on page:", result.error_message)
    
    # Save the aggregated job listings to a JSON file
    with open("linkedin_jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_extracted_jobs, f, indent=4)
    
    print("Extracted LinkedIn jobs saved to linkedin_jobs.json")

if __name__ == "__main__":
    asyncio.run(main())

