# Description: program/test_program.py

## Overview
Automated integration test script verifying that the local database control portal successfully creates, updates, lists, exports, and deletes database records through its REST endpoints.

## Exports & Functions
- `test_manager_suite()`
  - **Description**: Tests all manager API routes using Starlette TestClient.
  - **Parameters**: None.
  - **Returns**: None.

## Dependencies & Data Flow
- **Imports**: `starlette.testclient.TestClient`, `program.main.app`.
- **Invoked By**: Terminal execution (`python program/test_program.py`).
- **Data Flow**: Test queries -> Manager endpoints -> Repository -> Assert results.
