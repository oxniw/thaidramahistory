# ==============================================================================
# File: .//Description-of-file/test_suite.md
# Overview: Automated integration and unit test suite verifying endpoints and CRUD.
# ==============================================================================

import sys
from fastapi.testclient import TestClient
from main import app
from config import settings


def run_all_tests():
    """Run sequential integration checks across all routes and security gates."""
    print("==================================================")
    print("STARTING NOTICE BOARD TEST SUITE")
    print("==================================================")

    with TestClient(app) as client:
        # 1. Health Probe
        print("[1/6] Testing GET /health...")
        health_res = client.get("/health")
        assert health_res.status_code == 200, f"Health probe failed: {health_res.text}"
        assert health_res.json()["status"] == "ok"
        print("  OK - Health probe returned 200 with status 'ok'.")

        # 2. Static Asset Delivery
        print("[2/6] Testing static file serving...")
        root_res = client.get("/")
        assert root_res.status_code == 200, "Root path failed to serve index.html"
        assert "NOTICE BOARD" in root_res.text
        assert client.get("/static/styles.css").status_code == 200
        assert client.get("/static/app.js").status_code == 200
        print("  OK - Frontend HTML, CSS, and JS assets served correctly.")

        # 3. List Notices & Filters
        print("[3/6] Testing GET /api/notices...")
        notices_res = client.get("/api/notices")
        assert notices_res.status_code == 200
        notices = notices_res.json()
        assert len(notices) >= 5, f"Expected at least 5 seed notices, found {len(notices)}"

        # Test Search Filter
        search_res = client.get("/api/notices?search=Broadcast")
        assert search_res.status_code == 200
        assert len(search_res.json()) >= 1
        print("  OK - Public notice listing and keyword filtering working.")

        # 4. Admin Security Verification
        print("[4/6] Testing Admin Authorization Gates...")
        # Missing key should return 401
        res_missing = client.post("/api/notices", json={"title": "Hack", "content": "Test"})
        assert res_missing.status_code == 401, f"Expected 401 for missing key, got {res_missing.status_code}"

        # Wrong key should return 403
        res_wrong = client.post(
            "/api/notices",
            headers={"X-Admin-Key": "invalid-passkey"},
            json={"title": "Hack", "content": "Test"},
        )
        assert res_wrong.status_code == 403, f"Expected 403 for wrong key, got {res_wrong.status_code}"

        # Verify endpoint check
        verify_ok = client.get("/api/auth/verify", headers={"X-Admin-Key": settings.ADMIN_API_KEY})
        assert verify_ok.status_code == 200
        print("  OK - Unauthorized requests blocked (401/403); valid passkey accepted.")

        # 5. Create Notice (POST)
        print("[5/6] Testing Notice Creation (POST /api/notices)...")
        new_payload = {
            "title": "Integration Test Notice",
            "content": "This notice was generated automatically by the test suite.",
            "category": "Testing",
            "priority": "urgent",
            "is_pinned": True,
            "author": "Automated Tester",
        }
        create_res = client.post(
            "/api/notices",
            headers={"X-Admin-Key": settings.ADMIN_API_KEY},
            json=new_payload,
        )
        assert create_res.status_code == 201, f"Create notice failed: {create_res.text}"
        created_data = create_res.json()
        notice_id = created_data["id"]
        assert created_data["title"] == new_payload["title"]
        assert created_data["is_pinned"] is True
        print(f"  OK - Created notice with ID: {notice_id}")

        # 6. Update (PUT) and Delete (DELETE)
        print("[6/6] Testing Notice Update & Deletion...")
        # Update
        update_res = client.put(
            f"/api/notices/{notice_id}",
            headers={"X-Admin-Key": settings.ADMIN_API_KEY},
            json={"title": "Updated Test Notice", "is_pinned": False},
        )
        assert update_res.status_code == 200
        assert update_res.json()["title"] == "Updated Test Notice"
        assert update_res.json()["is_pinned"] is False

        # Delete
        delete_res = client.delete(
            f"/api/notices/{notice_id}",
            headers={"X-Admin-Key": settings.ADMIN_API_KEY},
        )
        assert delete_res.status_code == 200

        # Verify deletion returns 404
        get_deleted = client.get(f"/api/notices/{notice_id}")
        assert get_deleted.status_code == 404
        print("  OK - Update and delete operations completed and verified.")

    print("==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as exc:
        print(f"TEST FAILED: {exc}")
        sys.exit(1)
