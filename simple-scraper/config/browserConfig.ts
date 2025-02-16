// Browser configuration settings for bypassing detection
// These settings help evade anti-bot measures and website security

import { type Browser } from "puppeteer";
import { type ParsedProxy } from "../types";

export function getBrowserLaunchOptions(
  proxyEnabled: boolean,
  parsedProxy?: ParsedProxy
) {
  // Configure browser to avoid detection
  const launchOptions: any = {
    headless: true,
    args: [
      // Disable automation flags to prevent detection
      "--disable-blink-features=AutomationControlled",
      // Bypass OS security restrictions
      "--no-sandbox",
      "--disable-setuid-sandbox",
    ],
    // Bypass SSL/TLS certificate validation
    ignoreHTTPSErrors: true,
  };

  // Add proxy configuration if enabled
  if (proxyEnabled && parsedProxy) {
    launchOptions.args.push(
      `--proxy-server=${parsedProxy.host}:${parsedProxy.port}`
    );
  }

  return launchOptions;
}

export async function setupPage(browser: Browser, parsedProxy?: ParsedProxy) {
  const page = await browser.newPage();

  // Mask automation fingerprint with realistic user agent
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
  );

  // Set up proxy authentication if needed
  if (parsedProxy) {
    await page.authenticate({
      username: parsedProxy.username,
      password: parsedProxy.password,
    });
  }

  return page;
}
