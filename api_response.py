import requests

# Example: Public API (JSON placeholder for testing)
url = "https://jsonplaceholder.typicode.com/todos/1"

# Make the request
response = requests.get(url)  # <- this was missing

# Check status code
if response.status_code == 200:
    data = response.json()  # Convert JSON to Python dictionary
    print("Title:", data["title"])
else:
    print("Error:", response.status_code)

