// Main entry point for the scraping demonstration
// This file orchestrates the entire scraping process with security bypass techniques

import type { ProxyConfig } from "../types";
import { toggleProxy } from "../utils/proxyUtils";
import { formatResults, runConcurrentRequests } from "./scraper";


// Initialize proxy configuration
const proxyConfig: ProxyConfig = {
  enabled: false,
  url: process.env.PROXY_URL || "",
};

async function demonstrateProxy() {
  const targetUrl = "https://seoia.com.br/secure";
  
  console.log("\n🔍 Starting scraping demonstration");
  console.log("Target URL:", targetUrl);

  // Test without proxy (baseline)
  console.log("\n📡 Testing without proxy...");
  let results = await runConcurrentRequests(targetUrl, 7, proxyConfig);
  formatResults(results);

  // Test with proxy enabled
  if (proxyConfig.url) {
    const updatedConfig = toggleProxy(proxyConfig, true);
    results = await runConcurrentRequests(targetUrl, 7, updatedConfig);
    formatResults(results);
  } else {
    console.log("\n⚠️ No proxy URL configured. Skipping proxy tests.");
    console.log("To test with a proxy, set the PROXY_URL environment variable.");
  }
}

// Start the demonstration
demonstrateProxy();
