
---

# Human-Like Web Scraper

This project provides a web scraper that leverages human-like behavior and stealth techniques to extract table data from a target webpage. The scraper uses a headless browser approach, randomized HTTP headers, human-like delays, and simulated user interactions to reduce the chance of detection.

> **Disclaimer:** Ensure that your scraping activities comply with the target website's terms of service and applicable laws.

## Features

- **Randomized Headers and User Agents:** Rotates through common browser headers to mimic different users.
- **Human-Like Delays:** Introduces random delays between actions to simulate natural browsing behavior.
- **Script Injection for Simulated Mouse Movements:** Injects a JavaScript snippet to mimic mouse movements.
- **Proxy Support:** Uses a configurable proxy server to route requests.
- **LLM-Based Extraction:** Uses an LLM extraction strategy (via `crawl4ai`) to extract table data as JSON.

## Prerequisites

- **Python:** Version 3.7 or higher is required.
- **Dependencies:**  
  Install the following Python packages:
  - `crawl4ai`
  - `pydantic`
  
  You can install them with pip:
  ```bash
  pip install crawl4ai pydantic
  ```

## Setup and Configuration

1. **Clone or Download the Project:**

   Clone the repository or download the script file to your local machine.

2. **Proxy Configuration:**

   Update the `proxy_config` dictionary in the script with your proxy details:
   ```python
   proxy_config = {
       "server": "http://your-proxy-server:port",
       "username": "your_username",
       "password": "your_password",
   }
   ```

3. **Target URL and Extraction Settings:**

   - The URL to be scraped is defined as `URL_TO_SCRAPE`. Modify this variable to change the target page.
   - The LLM extraction strategy is set up using `LLMExtractionStrategy` in the script. Adjust the `provider`, `schema`, and `instruction` as needed.

## How to Run

Simply run the script using Python:
```bash
python main.py
```

### What the Script Does

1. **Simulated Delays and Interactions:**  
   The script introduces a random delay and injects JavaScript to simulate a mouse movement, making the interaction more human-like.

2. **Web Crawling and Data Extraction:**  
   The configured crawler then accesses the target URL, extracts table data, and processes it into JSON using an LLM-based extraction strategy.

3. **Output:**  
   Extracted data is printed to the console.

## Extending the Script

- **Additional Simulated Interactions:**  
  You can extend the script to simulate scrolling, key presses, or more advanced user behaviors by injecting additional JavaScript or using other browser automation features.
  
- **Persistent Cookies and Sessions:**  
  To mimic returning users, you might add functionality to save and load cookies between sessions.
  
- **Proxy Rotation:**  
  For higher anonymity, consider integrating a proxy pool that rotates proxies between requests.

## Troubleshooting

- **Extraction Issues:**  
  If the JSON extraction fails, verify that the webpage's structure aligns with your extraction strategy and that the LLM extraction parameters are correctly configured.

- **Proxy Problems:**  
  Ensure that your proxy server is accessible and that the provided credentials (if any) are correct.

## License

Include your project license information here.

## Disclaimer

The techniques used in this project are for educational purposes only. Use these methods responsibly and ensure you are compliant with all relevant legal and ethical guidelines.

---

This README provides the essential information needed to set up, configure, and run the human-like web scraper without the need for an external `requirements.txt`.
