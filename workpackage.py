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
        "testTypeName": "S-CV_Capacitance and Rgint",
        "testType" : 1025,
        "samples" : [{
                    "product" : 1213,
                    "number" : 1,
                    "owner" : "shak1kor",
                    # "customerSampleList" : "10000T001",
                    "def62" : "Dummy",
                    "def68" : "Active",
                    "def76" : "TV3e",
                    "sampleStatusByTest": 10,
                    "sampleStatusByTestLabel": "Assigned"
        },
        {
                    "product" : 1204,
                    "number" : 1,
                    "owner" : "shak1kor",
                    # "customerSampleList" : "10000T001",
                    "def62" : "Dummy",
                    "def68" : "Active",
                    "def76" : "TV4",
                    "sampleStatusByTest": 10,
                    "sampleStatusByTestLabel": "Assigned"
        }]
}

payload = json.dumps(data)
response = requests.post(url, headers=headers,json=data,verify=False)

# Check the response
if response.status_code == 200:
    print(f"Test added successfully!")
else:
    print("Error adding test:", response.text)