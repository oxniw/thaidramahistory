# ==============================================================================
# File: .//Description-of-file/program_test.md
# Overview: Automated integration test suite for the local database control portal.
# ==============================================================================

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from program.main import app


def test_manager_suite():
    """Verify local manager CRUD, export, and static serving."""
    print("==================================================")
    print("STARTING PROGRAM MANAGER TEST SUITE")
    print("==================================================")

    with TestClient(app) as client:
        # 1. Dashboard UI
        print("[1/5] Testing Manager Dashboard HTML serving...")
        root_res = client.get("/")
        assert root_res.status_code == 200
        assert "THAIDRAMAHISTORY CONTROL" in root_res.text
        print("  OK - Manager frontend served.")

        # 2. List Notices
        print("[2/5] Testing GET /api/notices...")
        list_res = client.get("/api/notices")
        assert list_res.status_code == 200
        records = list_res.json()
        assert isinstance(records, list)
        print(f"  OK - Retrieved {len(records)} record(s) from database.")

        # 3. Create Notice
        print("[3/5] Testing POST /api/notices...")
        new_item = {
            "title": "Manager Automated Test Notice",
            "content": "Created via local database control portal.",
            "category": "Testing",
            "priority": "urgent",
            "is_pinned": True,
            "author": "Control Suite",
        }
        create_res = client.post("/api/notices", json=new_item)
        assert create_res.status_code == 201, create_res.text
        created = create_res.json()
        notice_id = created["id"]
        assert created["title"] == new_item["title"]
        print(f"  OK - Created record: {notice_id}")

        # 4. Update & Export
        print("[4/5] Testing PUT & GET /api/export...")
        update_res = client.put(f"/api/notices/{notice_id}", json={"title": "Updated Title"})
        assert update_res.status_code == 200
        assert update_res.json()["title"] == "Updated Title"

        export_res = client.get("/api/export")
        assert export_res.status_code == 200
        assert export_res.headers["content-type"] == "application/json"
        print("  OK - Update and JSON backup export verified.")

        # 5. Delete Notice
        print("[5/5] Testing DELETE /api/notices/{id}...")
        del_res = client.delete(f"/api/notices/{notice_id}")
        assert del_res.status_code == 200
        print("  OK - Record deleted successfully.")

    print("==================================================")
    print("ALL MANAGER TESTS PASSED!")
    print("==================================================")


if __name__ == "__main__":
    try:
        test_manager_suite()
    except Exception as exc:
        print(f"FAILED: {exc}")
        sys.exit(1)
