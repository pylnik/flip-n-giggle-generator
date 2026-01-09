/**
 * Get the API base URL from environment variables
 * @returns {string} The API base URL (empty string for local proxy, or full URL for production)
 */
export function getApiBaseUrl() {
  // In development, if VITE_API_BASE_URL is not set, return empty string to use Vite's proxy
  // In production, VITE_API_BASE_URL should be set to the actual server domain
  const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
  
  // Remove trailing slash if present
  return baseUrl.replace(/\/$/, '')
}

/**
 * Construct the full API URL for a given endpoint
 * @param {string} endpoint - The API endpoint (e.g., '/api/phrases/en')
 * @returns {string} The full API URL
 */
export function getApiUrl(endpoint) {
  const baseUrl = getApiBaseUrl()
  
  // Ensure endpoint starts with /
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  
  return `${baseUrl}${normalizedEndpoint}`
}
