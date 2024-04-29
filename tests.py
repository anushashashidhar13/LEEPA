from urllib.request import urlopen 
import requests
import json


url = "https://cz.leepa.app.bosch.com/en/aeepc/api2/tests"

headers = {
        'Authorization': 'Bearer NTQ7ITppQGs7NTM7dFk4M0tVMENCVktBKnBjRmoocGw1dTE7SDpnSyghMUdwZEgxNjkpSFRUY2JaZEZIc0d4UDRQaA==',  # Assuming it's a Bearer token
        'Content-Type': 'application/json'  # Modify the content type if necessary
    }

data = {
    "order" : "VA2400075",
    "testType" : 1014,
    
}

response = requests.post(url, headers=headers,json=data,verify=False)

# Check the response
if response.status_code == 200:
    print(f"Test added successfully!")
else:
    print("Error adding test:", response.text)