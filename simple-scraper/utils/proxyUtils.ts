// Utilities for handling proxy configuration and management
// These functions help bypass proxy detection and maintain anonymity

import { type ParsedProxy, type ProxyConfig } from '../types';

// Parse proxy URL to extract authentication and location data
// This helps in rotating proxies and maintaining anonymous access
export function parseProxyUrl(proxyUrl: string): ParsedProxy {
  const [protocol, rest] = proxyUrl.split("://");
  const [host, port, username, rawPassword] = rest.split(":");
  const [password, ...options] = rawPassword.split("_");

  // Parse additional proxy options for enhanced anonymity
  const optionsMap: { [key: string]: string } = {};
  options.forEach((opt) => {
    const [key, value] = opt.split("-");
    optionsMap[key] = value;
  });

  return {
    protocol,
    host,
    port: parseInt(port),
    username,
    password,
    country: optionsMap.country,
  };
}

// Manage proxy state and provide feedback on proxy status
export function toggleProxy(proxyConfig: ProxyConfig, enable: boolean = !proxyConfig.enabled): ProxyConfig {
  const updatedConfig = { ...proxyConfig, enabled: enable };
  
  if (enable && updatedConfig.url) {
    const { country } = parseProxyUrl(updatedConfig.url);
    updatedConfig.country = country;
    console.log(`\n🔒 Proxy enabled (Country: ${country || "unknown"})`);
  } else {
    console.log("\n🔓 Proxy disabled");
  }
  
  return updatedConfig;
}
