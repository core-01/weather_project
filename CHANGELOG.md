# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-30
- Initial "build" release: feature-complete backend proxy for Weather API.
- Implemented endpoints: current, forecast, future, history, marine, search, ip, timezone, astronomy.
- Added DB persistence of raw API responses and metadata (`params_json`, `response_time_ms`, `status_code`, `request_url`).
- Added optional Redis caching helper.
- Added retries, logging, and request timing for external API calls.
- Added pytest tests and GitHub Actions CI (lint, type-check, tests, coverage).
