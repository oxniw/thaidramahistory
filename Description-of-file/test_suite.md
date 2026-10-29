# Description: test_suite.py

## Overview
Automated integration and unit test suite verifying health probes, static assets, model validations, admin authorization, and full CRUD operations.

## Exports & Functions
- `run_all_tests()`
  - **Description**: Executes sequential endpoint assertions against the FastAPI app using Starlette TestClient.
  - **Parameters**: None.
  - **Returns**: None (raises AssertionError on failure).

## Dependencies & Data Flow
- **Imports**: `starlette.testclient.TestClient`, `main.app`, `config.settings`.
- **Invoked By**: Terminal command (`python test_suite.py`).
- **Data Flow**: Test payloads -> FastAPI endpoints -> Service validation -> Assert response codes and data integrity.
