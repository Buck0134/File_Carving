import requests

response = requests.get('http://127.0.0.1:5000/data')

if response.status_code == 200:
    print(response.json())
else:
    print("Failed to retrieve data")
