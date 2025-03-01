import asyncio
import json
import os
import random
from typing import List

from crawl4ai import (AsyncWebCrawler, BrowserConfig, CacheMode,
                      CrawlerRunConfig)
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

URL_TO_SCRAPE = "https://seoia.com.br/secure"
INSTRUCTION_TO_LLM = "Extract all the table data into a JSON"

class Product(BaseModel):
    name: str
    price: str

# List of common user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
]

proxy_config = {
    "server": "http://premium-residential.evomi.com:8080",
    "username": "",
    "password": "",
}

def get_random_headers():
    """Generate randomized HTTP headers to mimic a real browser."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

async def human_like_delay(min_delay=2, max_delay=5):
    """Introduce a random delay to simulate human browsing behavior."""
    delay = random.uniform(min_delay, max_delay)
    print(f"Sleeping for {delay:.2f} seconds to mimic human-like browsing...")
    await asyncio.sleep(delay)

async def simulate_mouse_movement(crawler):
    """Inject JavaScript to simulate a human-like mouse movement."""
    simulate_mouse_script = """
    (() => {
      let startX = Math.random() * window.innerWidth;
      let startY = Math.random() * window.innerHeight;
      document.dispatchEvent(new MouseEvent('mousemove', {
          clientX: startX,
          clientY: startY,
          bubbles: true
      }));
    })();
    """
    # Inject the script into the page. This assumes your crawler supports script injection.
    try:
        await crawler.inject_script(simulate_mouse_script)
        print("Injected simulated mouse movement script.")
    except Exception as e:
        print("Error injecting script:", e)

async def main():
    # Create the LLM extraction strategy with provided schema
    llm_strategy = LLMExtractionStrategy(
        provider="ollama/deepseek-r1:14b",
        schema=Product.model_json_schema(),
        extraction_type="schema",
        instruction=INSTRUCTION_TO_LLM,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format="markdown",
        extra_args={"temperature": 0.0, "max_tokens": 800},
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS,
        process_iframes=False,
        remove_overlay_elements=True,
        exclude_external_links=True,
        headers=get_random_headers()  # Pass randomized headers
    )

    browser_cfg = BrowserConfig(proxy_config=proxy_config)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # Simulate human-like delay before starting
        await human_like_delay()

        # Optionally, simulate a mouse movement before extraction to mimic user behavior.
        await simulate_mouse_movement(crawler)

        result = await crawler.arun(url=URL_TO_SCRAPE, config=crawl_config)

        if result.success:
            try:
                data = json.loads(result.extracted_content)
                print("Extracted items:", data)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
            llm_strategy.show_usage()
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
