import requests

try:
    response = requests.get("http://127.0.0.1:8000/docs")
    if response.status_code == 200:
        print("Service found on port 8000")
    else:
        print(f"Service on port 8000 returned status: {response.status_code}")
except Exception as e:
    print(f"Failed to connect to port 8000: {e}")
