import asyncio
import json
import os
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


proxy_config = {
    "server": "http://premium-residential.evomi.com:8080",
    "username": "",
    "password": "",
}


async def main():

    llm_strategy = LLMExtractionStrategy(
        provider="ollama/deepseek-r1:14b",
        # api_token=os.getenv("OPENAI_API_KEY"),
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
    )

    browser_cfg = BrowserConfig(proxy_config=proxy_config)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:

        result = await crawler.arun(url=URL_TO_SCRAPE, config=crawl_config)

        if result.success:
            data = json.loads(result.extracted_content)

            print("Extracted items:", data)

            llm_strategy.show_usage()
        else:
            print("Error:", result.error_message)


if __name__ == "__main__":
    asyncio.run(main())
