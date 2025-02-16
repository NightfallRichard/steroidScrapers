// Main scraper functionality with anti-detection measures
// This module orchestrates the scraping process while bypassing security measures

import puppeteer from "puppeteer";
import { getBrowserLaunchOptions, setupPage } from "../config/browserConfig";
import { type ProxyConfig, type RequestResult } from "../types";
import { parseProxyUrl } from "../utils/proxyUtils";

export async function makeRequest(
  url: string,
  requestNumber: number,
  proxyConfig: ProxyConfig
): Promise<RequestResult> {
  const parsedProxy = proxyConfig.enabled
    ? parseProxyUrl(proxyConfig.url)
    : undefined;
  const browser = await puppeteer.launch(
    getBrowserLaunchOptions(proxyConfig.enabled, parsedProxy)
  );

  try {
    const page = await setupPage(browser, parsedProxy);

    // Get IP information to verify proxy effectiveness
    const ip = await page.evaluate(async () => {
      const response = await fetch("https://api.ipify.org?format=json");
      const data = await response.json();
      return data.ip;
    });

    // Verify geolocation for proxy effectiveness
    let country: string | undefined;
    if (proxyConfig.enabled && proxyConfig.country) {
      country = proxyConfig.country;
    } else {
      try {
        const response = await fetch(
          `https://ipinfo.io/${ip}/json?token=${process.env.IPINFO_TOKEN}`
        );
        const data = await response.json();
        country = data.country;
      } catch (error) {
        console.log("⚠️ Failed to get country info");
      }
    }

    // Navigate with anti-detection measures
    await page.goto(url, {
      waitUntil: "networkidle0", // Wait for network to be idle to bypass lazy-loading protection
      timeout: 30000,
    });

    // Wait for potential anti-bot challenges to load
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Bypass content protection mechanisms
    await page.evaluate(() => {
      const content = document.getElementById("secure-content");
      if (content) {
        content.style.display = "block";
      }
    });

    // Wait for protected content while avoiding detection
    try {
      await page.waitForFunction(
        () => {
          const text = document.body.innerText;
          return (
            text.includes("Secure Page") &&
            text.includes("Welcome to the secure page")
          );
        },
        { timeout: 5000 }
      );
    } catch (_) {
      // Silently handle timeouts to avoid leaving traces
    }

    const text = await page.evaluate(() => document.body.innerText);
    const success = text.includes("Welcome to the secure page");

    return {
      success,
      ip,
      country,
      requestNumber,
      response: text,
    };
  } catch (error) {
    return {
      success: false,
      ip: "unknown",
      error,
      requestNumber,
    };
  } finally {
    await browser.close();
  }
}

// Format results for analysis of scraping effectiveness
export function formatResults(results: RequestResult[]) {
  const successCount = results.filter((r) => r.success).length;
  console.log("\n📊 Results Summary:");
  console.log(
    `Success Rate: ${((successCount / results.length) * 100).toFixed(1)}%`
  );

  results.forEach((result) => {
    const status = result.success ? "✅" : "❌";
    const location = result.country ? ` (${result.country})` : "";
    const text = result.response
      ? ` - ${result.response.replace(/\n/g, " ").trim()}`
      : "";
    console.log(
      `${status} Request ${result.requestNumber}: IP ${result.ip}${location}${text}`
    );
    if (result.error) {
      console.log(`   Error: ${result.error.message}`);
    }
  });
}

// Run multiple requests concurrently to distribute traffic patterns
export async function runConcurrentRequests(
  url: string,
  count: number,
  proxyConfig: ProxyConfig
) {
  const requests = Array.from({ length: count }, (_, i) =>
    makeRequest(url, i + 1, proxyConfig)
  );
  return Promise.all(requests);
}
