# Web Scraper with AI-Powered Data Extraction

This project demonstrates an asynchronous web scraping tool that leverages AI (via Ollama's LLM) to extract structured data from websites. It uses the `crawl4ai` library to crawl web pages and extract table data into a JSON format using Pydantic models.

## Features

- 🕷️ Asynchronous web crawling
- 🤖 LLM-powered data extraction (using Ollama's deepseek-r1:14b model)
- 🧱 Pydantic model validation
- 🔄 Proxy support for residential proxies
- 📦 Caching mechanisms
- 🖥️ Headless browser automation
- 🧩 Chunk processing for large content

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/web-scraper-ai.git
cd web-scraper-ai
```

2. Install dependencies:
```bash
pip install crawl4ai pydantic asyncio python-dotenv
```

3. Install Ollama (required for local LLM processing):
```bash
# Follow instructions from https://ollama.ai/download
```

4. Pull the LLM model:
```bash
ollama pull deepseek-r1:14b
```

## Usage

### Basic Configuration
1. Create a `.env` file for environment variables:
```env
OPENAI_API_KEY=your_api_key_here  # Only needed if using OpenAI models
```

2. Modify the script with your target URL and proxy configuration:
```python
URL_TO_SCRAPE = "https://your-target-website.com"
proxy_config = {
    "server": "http://your-proxy-server:port",
    "username": "your-username",
    "password": "your-password",
}
```

### Running the Scraper
```bash
python main.py
```

## Configuration Options

### LLM Extraction Strategy
```python
LLMExtractionStrategy(
    provider="ollama/deepseek-r1:14b",  # Can use "openai/gpt-4" for OpenAI
    api_token=os.getenv("OPENAI_API_KEY"),
    schema=Product.model_json_schema(),
    extraction_type="schema",
    instruction="Extract all the table data into a JSON",
    # ... other parameters
)
```

### Crawler Configuration
```python
CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    process_iframes=False,
    remove_overlay_elements=True,
    exclude_external_links=True
)
```

### Proxy Configuration
```python
proxy_config = {
    "server": "http://proxy-server:port",
    "username": "your-username",
    "password": "your-password"
}
```

## Dependencies

- Python 3.9+
- crawl4ai
- pydantic
- asyncio
- python-dotenv
- Ollama (for local LLM processing)

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [crawl4ai](https://github.com/yourhandle/crawl4ai) - Web crawling library
- [Ollama](https://ollama.ai/) - Local LLM processing
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Note:** Always ensure you have proper authorization before scraping any website. Respect robots.txt rules and website terms of service.
