import requests
import json
import datetime
import pandas as pd
import time

def scan_data():
    #Fetches scan data from the API, parses it to a DataFrame, and returns it."""
    # Could've used refresh token to avoid overusing auth api call.
    auth_url = "removed"
    auth_headers = {"Content-Type": "application/json"}
    ident = "company id"
    username = "username" # Had to use hardcoded credentials for lack of better options, ideally would've deployed on Azure or a local server.
    password = "password"    
    auth_request_body = {"ident": ident, "username": username, "password": password}
    api_url = "removed"

    access_token = authenticate(auth_url, auth_headers, auth_request_body)
    if not access_token:
        print("Authentication failed!")
        return None
    
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    request_body = {
        "PageNumber": 0,
        "SortField": "createDate",
        "SortAscending": True,
        "GroupSortField": "",
        "GroupSortAscending": True,
        "DisplayedProperties": [
          "barcode",
          "productName",
          "quantity",
          "direction",
          "fullName",
          "refCode",
          "createDate",
          "createTime",
          "warehouseName"
        ],
        "FilterItems": [
          {
            "FieldId": "create_date",
            "Negate": False,
            "Condition": 2,
            "Criteria1": "2024-01-01",
            "Criteria2": datetime.datetime.now().strftime("%Y-%m-%d")
          },
          {
            "FieldId": "direction",
            "Negate": False,
            "Condition": 1,
            "Criteria1": "Outgoing"
          },
          {
            "FieldId": "warehouse_id",
            "Negate": False,
            "Condition": 0,
            "Criteria1": [571] 
          }
        ]
    }
    response_content = call_api(api_url, headers, request_body)

    if not response_content:
        return None

    try:
        json_response = json.loads(response_content)
        items = json_response["items"]
        df_scanlog = pd.DataFrame(items).drop(columns=['productId', 'itemId', 'transportId'])
        print("Scan data fetched successfully:", datetime.datetime.now())
        return df_scanlog
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing response: {e}")
        return None     
    
def authenticate(auth_url, auth_headers, auth_request_body):
    try:
        with requests.post(auth_url, headers=auth_headers, json=auth_request_body) as response:
            response.raise_for_status()
            return response.json()["accessToken"]
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return None

def call_api(api_url, headers, request_body):
    try:
        response = requests.post(api_url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return None