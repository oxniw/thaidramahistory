# ==============================================================================
# File: .//Description-of-file/test_suite.md
# Overview: Automated integration and unit test suite verifying read-only board.
# ==============================================================================

import sys
from fastapi.testclient import TestClient
from main import app


def run_all_tests():
    """Run sequential integration checks across all routes and security gates."""
    print("==================================================")
    print("STARTING READ-ONLY THAIDRAMAHISTORY TEST SUITE")
    print("==================================================")

    with TestClient(app) as client:
        # 1. Health Probe (without leaking internal server environment)
        print("[1/5] Testing GET /health...")
        health_res = client.get("/health")
        assert health_res.status_code == 200, f"Health probe failed: {health_res.text}"
        assert health_res.json() == {"status": "ok"}
        print("  OK - Health probe returned 200 without exposing server metadata.")

        # 2. Static Asset Delivery
        print("[2/5] Testing static file serving...")
        root_res = client.get("/")
        assert root_res.status_code == 200, "Root path failed to serve index.html"
        assert "THAIDRAMAHISTORY" in root_res.text
        assert client.get("/static/styles.css").status_code == 200
        assert client.get("/static/app.js").status_code == 200
        print("  OK - Frontend HTML, CSS, and JS assets served correctly.")

        # 3. List Notices & Filters
        print("[3/5] Testing GET /api/notices...")
        notices_res = client.get("/api/notices")
        assert notices_res.status_code == 200
        notices = notices_res.json()
        assert len(notices) >= 5, f"Expected at least 5 notices, found {len(notices)}"

        # Test Search Filter
        search_res = client.get("/api/notices?search=Broadcast")
        assert search_res.status_code == 200
        assert len(search_res.json()) >= 1

        # Test Priority Filter
        urgent_res = client.get("/api/notices?priority=urgent")
        assert urgent_res.status_code == 200
        for item in urgent_res.json():
            assert item["priority"] == "urgent"
        print("  OK - Public notice listing and keyword/priority filtering verified.")

        # 4. Single Notice Retrieval
        print("[4/5] Testing GET /api/notices/{id}...")
        first_notice_id = notices[0]["id"]
        single_res = client.get(f"/api/notices/{first_notice_id}")
        assert single_res.status_code == 200
        assert single_res.json()["id"] == first_notice_id

        # 404 on non-existent notice
        not_found_res = client.get("/api/notices/nonexistent123456789012")
        assert not_found_res.status_code == 404
        print("  OK - Single notice retrieval and 404 handling verified.")

        # 5. Security: Verify No Mutation Endpoints Exist (No Server Manipulation)
        print("[5/5] Testing that mutating endpoints are disabled (405 Method Not Allowed)...")
        post_attempt = client.post("/api/notices", json={"title": "Test", "content": "Test"})
        assert post_attempt.status_code == 405, f"Expected 405, got {post_attempt.status_code}"

        put_attempt = client.put(f"/api/notices/{first_notice_id}", json={"title": "Test"})
        assert put_attempt.status_code == 405, f"Expected 405, got {put_attempt.status_code}"

        delete_attempt = client.delete(f"/api/notices/{first_notice_id}")
        assert delete_attempt.status_code == 405, f"Expected 405, got {delete_attempt.status_code}"
        print("  OK - All mutation routes are disabled (HTTP 405). Server cannot be manipulated.")

    print("==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as exc:
        print(f"TEST FAILED: {exc}")
        sys.exit(1)
