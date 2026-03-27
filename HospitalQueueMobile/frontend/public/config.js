/**
 * API Configuration for Hospital Queue Mobile App
 * 
 * This file manages the API base URL for connecting to the Flask backend.
 * The URL can be changed at runtime via the Settings UI in the app.
 */

// Default API base URL - change this to your computer's IP address
// Format: "http://192.168.x.y:5000" (replace x.y with your actual IP)
// To find your IP: 
//   Windows: ipconfig (look for IPv4 Address)
//   Mac/Linux: ifconfig or ip addr
const DEFAULT_API_BASE_URL = "http://192.168.1.100:5000";

// Storage key for saved API URL
const API_URL_STORAGE_KEY = "hospital_queue_api_url";

/**
 * Get the API base URL from localStorage or use default
 * @returns {string} API base URL
 */
function getApiBaseUrl() {
  try {
    const savedUrl = localStorage.getItem(API_URL_STORAGE_KEY);
    if (savedUrl && savedUrl.trim() !== "") {
      return savedUrl.trim();
    }
  } catch (e) {
    console.warn("Could not read API URL from localStorage:", e);
  }
  return DEFAULT_API_BASE_URL;
}

/**
 * Save the API base URL to localStorage
 * @param {string} url - API base URL to save
 */
function setApiBaseUrl(url) {
  try {
    if (url && url.trim() !== "") {
      // Remove trailing slash if present
      const cleanUrl = url.trim().replace(/\/+$/, "");
      localStorage.setItem(API_URL_STORAGE_KEY, cleanUrl);
      return true;
    }
  } catch (e) {
    console.error("Could not save API URL to localStorage:", e);
  }
  return false;
}

/**
 * Get the full API endpoint URL
 * @param {string} endpoint - API endpoint (e.g., "/api/queue")
 * @returns {string} Full URL
 */
function getApiUrl(endpoint) {
  const baseUrl = getApiBaseUrl();
  // Ensure endpoint starts with /
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : "/" + endpoint;
  return baseUrl + cleanEndpoint;
}

// Export for use in other scripts
if (typeof window !== "undefined") {
  window.API_CONFIG = {
    getBaseUrl: getApiBaseUrl,
    setBaseUrl: setApiBaseUrl,
    getUrl: getApiUrl,
    DEFAULT_URL: DEFAULT_API_BASE_URL
  };
}



