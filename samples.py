from urllib.request import urlopen 
import requests
import json


url = "https://cz.leepa.app.bosch.com/en/aeepc/api2/samples"

headers = {
        'Authorization': 'Bearer NTQ7ITppQGs7NTM7dFk4M0tVMENCVktBKnBjRmoocGw1dTE7SDpnSyghMUdwZEgxNjkpSFRUY2JaZEZIc0d4UDRQaA==',  # Assuming it's a Bearer token
        'Content-Type': 'application/json'  # Modify the content type if necessary
    }

data = {
                "order" : 842,
                "product" : 1204,
                "number" : 1,
                "owner" : "shak1kor",
                "remark":"Adding samples",
                "def62" : "Dummy",
                "def68" : "Active",
                "test" : 5780
            }

payload = json.dumps(data)
response = requests.post(url, headers=headers,json=data,verify=False)

# Check the response
if response.status_code == 200:
    print(f"Sample created successfully!")
else:
    print("Error creating sample:", response.text)