# Test Configurations

Based on SOA principles of interoperability and standardized service contracts (SRC-25), the product must be tested across the configurations real users will have.

## Browsers (must test all)
- Chrome (latest) – Windows, Mac, Linux
- Firefox (latest)
- Safari (latest) – Mac only
- Edge (latest) – Windows

## Operating Systems
- Windows 10/11
- macOS (Ventura, Sonoma, Sequoia)
- Ubuntu 22.04/24.04

## Devices and screen sizes
- Desktop (1920x1080) – primary target
- Laptop (1366x768)
- Tablet (iPad, Android) – numbers may be too small; document as limitation

## Network conditions (for API health endpoint only)
- Fast (100 Mbps)
- Slow (3G throttled) – the Canvas renders client-side, so network mainly affects initial load

## Screen color profiles (manual testing only)
- Standard RGB
- sRGB
- HDR modes (may shift colors)

## Environmental conditions (manual)
- Bright sunlight (screen glare)
- Dark room (high contrast mode)

## API contract versions (future)
If the product exposes a REST API, it should follow SOA standardized service contract principles. The current version uses form POSTs with implicit contract. Before release, the API should be documented (OpenAPI) and versioned.

## Testing approach
- Automated cross-browser testing is not implemented due to time constraints.
- Manual testing covers Chrome, Firefox, and Safari on desktop.
- Load testing is automated with Locust (see specialized testing report).
