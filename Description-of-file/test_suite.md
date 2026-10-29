# Description: test_suite.py

## Overview
Automated integration and security test suite verifying health checks, static assets, database retrieval, search filters, and strict rejection of mutating HTTP methods (HTTP 405).

## Exports & Functions
- `run_all_tests()`
  - **Description**: Executes sequential endpoint assertions against the FastAPI app using Starlette TestClient.
  - **Parameters**: None.
  - **Returns**: None (raises AssertionError on failure).

## Dependencies & Data Flow
- **Imports**: `starlette.testclient.TestClient`, `main.app`.
- **Invoked By**: Terminal command (`python test_suite.py`).
- **Data Flow**: Test queries -> FastAPI endpoints -> Service validation -> Assert response codes and data integrity.
