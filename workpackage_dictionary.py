from urllib.request import urlopen 
import requests
import json
import pandas as pd
import re
import warnings

warnings.filterwarnings("ignore")

order_number = "VA2400075"
order_id = 842

# reading the excel sheet for data
df = pd.read_excel("C:/Users/SHAK1KOR/Desktop/Desktop_KOR-C-007DP/LEEPA/LEEPA_Importer_Template_latest.xlsx")

# read the header row from excel
header_list = df.columns.tolist()
header_dict = dict()
for i in range(1,len(header_list)+1):
    header_dict[i] = header_list[i-1]
check_val = df

# fetching the test name from sheet and finding its id and name from the tool
def fetch_test_id(url):
    data_dict = get_API_data(url) 
    tests = []
    
    for val in range(3,len(header_list)):
        test_val = header_list[val]
        
        test_ids = dict()
        inner_test = dict()
        for key,val in data_dict.items():
            current_test = data_dict[key]
            test_type = current_test["name"]
            leepa_substring = test_type.split('_')[0]
            excel_substring = test_val.split('_')[0]
            if excel_substring == leepa_substring:
                id = current_test["id"]
                test_name = current_test["name"]
                test_ids["name"] = test_name
                test_ids["id"] = id
                inner_test[test_val] = test_ids
                tests.append(inner_test)
            # test_type = test_type.replace('_', ' ')
            # test_type = test_type.replace('-', ' ')
            # words1 = test_type.split()
            # words2 = test_val.split('-')
            # if words1[0] == words2[0]:
            #     words1.pop(0)
            #     words2.pop(0)
            #     common_words = set(words1) & set(words2)
            #     test_ids = dict()
            #     inner_test = dict()
            #     if str(test_type).startswith(test_val[0:2]):
            #         id = current_test["id"]
            #         test_name = current_test["name"]
            #         test_ids["name"] = test_name
            #         test_ids["id"] = id
            #         inner_test[test_val] = test_ids
            #         tests.append(inner_test)
            #     elif common_words:
            #         id = current_test["id"]
            #         test_name = current_test["name"]
            #         test_ids["name"] = test_name
            #         test_ids["id"] = id
            #         inner_test[test_val] = test_ids
            #         tests.append(inner_test)
            #     else:
            #         words2 = re.findall('[A-Z][^A-Z]*', test_val)
            #         words2.pop(0)
            #         common_words = set(words1) & set(words2)
            #         if common_words:
            #             id = current_test["id"]
            #             test_name = current_test["name"]
            #             test_ids["name"] = test_name
            #             test_ids["id"] = id
            #             inner_test[test_val] = test_ids
            #             tests.append(inner_test)
    return tests

def workpackage_creation(order_number,test_name,test_id,sample_creation_list):

    url = "https://cz.leepa.app.bosch.com/en/aeepc/api2/tests"

    data = {
                "order" : order_number, 
                "testTypeName": test_name,
                "testType" : test_id,
                "samples" : sample_creation_list
    }
   
    status = post_JSON_data(url,data,"Test",test_name)

    return status

def get_API_data(url):

    headers = {
            'Authorization': 'Bearer NTQ7ITppQGs7NTM7dFk4M0tVMENCVktBKnBjRmoocGw1dTE7SDpnSyghMUdwZEgxNjkpSFRUY2JaZEZIc0d4UDRQaA==',  # Assuming it's a Bearer token
            'Content-Type': 'application/json'  # Modify the content type if necessary
        }
    
    response = requests.get(url,headers=headers,verify=False)

    if response.status_code == 200:
        json_text = json.loads(response.text)
        data = json_text['data']

    return data

def post_JSON_data(url,data,val,name):

    headers = {
            'Authorization': 'Bearer NTQ7ITppQGs7NTM7dFk4M0tVMENCVktBKnBjRmoocGw1dTE7SDpnSyghMUdwZEgxNjkpSFRUY2JaZEZIc0d4UDRQaA==',  # Assuming it's a Bearer token
            'Content-Type': 'application/json'  # Modify the content type if necessary
        }
    
    payload = json.dumps(data)
    response = requests.post(url, headers=headers,json=data,verify=False)

    # Check the response
    if response.status_code == 200 and val == "Test":
        print(f"Test {name} added successfully!")
    elif response.status_code == 200 and val == "Sample":
        print(f"Sample {name} added successfully!")
    else:
        print("Error :", response.text)

    return response.status_code

# iterating through the data frame
tests_dict = fetch_test_id("https://cz.leepa.app.bosch.com/en/aeepc/api2/test-types")

rows = len(df)
samples_url = "https://cz.leepa.app.bosch.com/en/aeepc/api2/products"
samples_type = get_API_data(samples_url)


# final_dict = {}
for col in df.columns[3:]:  
    col_dicts = []
    for index, row in df.iterrows():
        if row[col] == 1:
            sample = row["Product Type"]
            sample_dict = [i for i in samples_type if str(i["name"]).startswith(sample[0:1]) ]
            sample_id = sample_dict[0]["id"]
            sample_name = sample_dict[0]["name"]

            #sample type
            value = row["Samples type"]
            if value == "Rosinus":
                    sample_type = "Rosinius AMB"
            else:
                sample_type = value
            
            sample_list = row["Sample ID"]
            samples_creation_dict = {"product" : sample_id,
                                "number" : 1,
                                "owner" : "shak1kor",
                                # "customerSampleList" : "10000T001",
                                "def62" : "Dummy",
                                "def68" : "Active",
                                "def76" : sample_type,
                                "sampleStatusByTest": 10,
                                "sampleStatusByTestLabel": "Assigned"}
            col_dicts.append(samples_creation_dict)
    # final_dict[col] = col_dicts
    if col_dicts :
        dict = [i[col] for i in tests_dict if list(i.keys())[0] == col ]
        if col == "S-Static":
            testid_dict = [i for i in dict if i["id"] == 1020]
            test_name = testid_dict[0]["name"]
            test_id = testid_dict[0]["id"]
        elif col == "D-DoublePulse":
            testid_dict = [i for i in dict if i["id"] == 1012]
            test_name = testid_dict[0]["name"]
            test_id = testid_dict[0]["id"]
        else:
            test_name = dict[0]["name"]
            test_id = dict[0]["id"]
        val = workpackage_creation(order_number,test_name,test_id,col_dicts)
        if val == 200:
            print(f"Samples added to {test_name} Workpackage Successfully!!")
            print("\n")
    else:
        continue

print("All Done!!")