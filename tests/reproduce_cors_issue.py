import requests
import time
import sys
import subprocess
import os

def test_cors():
    url = "http://localhost:8360/"
    headers = {
        "Origin": "http://evil.com",
        "Access-Control-Request-Method": "GET"
    }

    print(f"Testing CORS on {url} with Origin: http://evil.com")

    try:
        # Test Preflight
        resp = requests.options(url, headers=headers)
        print(f"Preflight Status: {resp.status_code}")
        print(f"Preflight Headers: {resp.headers}")

        allow_origin = resp.headers.get("Access-Control-Allow-Origin")
        allow_creds = resp.headers.get("Access-Control-Allow-Credentials")

        print(f"Access-Control-Allow-Origin: {allow_origin}")
        print(f"Access-Control-Allow-Credentials: {allow_creds}")

        if allow_origin == "http://evil.com" and allow_creds == "true":
            print("VULNERABILITY CONFIRMED: Server allows arbitrary origin with credentials.")
            return True
        elif allow_origin == "*" and allow_creds == "true":
             print("VULNERABILITY CONFIRMED: Server allows all origins (*) with credentials (Note: Browsers might block this, but it's still permissive).")
             return True
        else:
            print("Vulnerability not detected or already fixed.")
            return False

    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

if __name__ == "__main__":
    test_cors()
