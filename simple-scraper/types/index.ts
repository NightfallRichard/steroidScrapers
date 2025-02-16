// Types for proxy configuration and request handling
// These types help us manage different proxy configurations for bypassing geo-restrictions and IP-based blocking

export interface ProxyConfig {
  enabled: boolean;
  url: string;
  country?: string;
}

// Structure for tracking request success and proxy effectiveness
export interface RequestResult {
  success: boolean;
  ip: string;
  error?: any;
  requestNumber: number;
  response?: string;
  country?: string;
}

// Parsed proxy configuration for authentication and location spoofing
export interface ParsedProxy {
  protocol: string;
  host: string;
  port: number;
  username: string;
  password: string;
  country?: string;
}
