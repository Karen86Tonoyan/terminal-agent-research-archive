import requests
import time
import sys
import subprocess
import os

def test_cors(origin, expected_allowed):
    url = "http://localhost:8360/"
    headers = {
        "Origin": origin,
        "Access-Control-Request-Method": "GET"
    }

    print(f"Testing CORS on {url} with Origin: {origin}")

    try:
        # Test Preflight
        resp = requests.options(url, headers=headers)
        print(f"Preflight Status: {resp.status_code}")

        allow_origin = resp.headers.get("Access-Control-Allow-Origin")
        allow_creds = resp.headers.get("Access-Control-Allow-Credentials")

        print(f"Access-Control-Allow-Origin: {allow_origin}")
        print(f"Access-Control-Allow-Credentials: {allow_creds}")

        if expected_allowed:
            if allow_origin == origin and allow_creds == "true":
                print(f"SUCCESS: {origin} is correctly allowed.")
                return True
            else:
                print(f"FAILURE: {origin} should be allowed but isn't.")
                return False
        else:
            if allow_origin is None:
                print(f"SUCCESS: {origin} is correctly blocked.")
                return True
            else:
                print(f"FAILURE: {origin} should be blocked but is allowed.")
                return False

    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

if __name__ == "__main__":
    print("--- Testing default allowed origin ---")
    s1 = test_cors("http://localhost:3000", True)

    print("\n--- Testing blocked origin ---")
    s2 = test_cors("http://evil.com", False)

    if s1 and s2:
        print("\nOVERALL STATUS: ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("\nOVERALL STATUS: TESTS FAILED")
        sys.exit(1)
