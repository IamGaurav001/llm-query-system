import requests

url = "http://localhost:8000/api/v1/hackrx/run"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
data = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment?"
    ]
}

r = requests.post(url, headers=headers, json=data)
print("Status Code:", r.status_code)
print("Response:", r.text)

try:
    print("JSON Response:", r.json())
except Exception as e:
    print("Could not decode JSON:", e)