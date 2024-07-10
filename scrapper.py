# %%
import requests
import json
from time import sleep
from tqdm import tqdm
import warnings
from rich import traceback

traceback.install()

warnings.filterwarnings("ignore")


def get_offers(offset=1, limit=30):
    url = "https://api.leboncoin.fr/api/adfinder/v1/search"

    payload = json.dumps(
        {
            "limit_alu": 2,
            "filters": {
                "category": {"id": "10"},
                "enums": {"ad_type": ["offer"], "real_estate_type": ["1", "2"]},
                "keywords": {"type": "all"},
                "location": {
                    "area": {"lat": 0, "lng": 0, "radius": 0},
                    "shippable": False,
                    "locations": [
                        {
                            "area": {
                                "default_radius": 9666,
                                "lat": 44.85027630256445,
                                "lng": -0.5749656849560539,
                                "radius": 5000,
                            },
                            "city": "Bordeaux",
                            "department_id": "33",
                            "label": "Bordeaux (toute la ville)",
                            "region_id": "2",
                            "locationType": "city",
                        }
                    ],
                },
                "owner": {"no_salesmen": False},
                "ranges": {},
            },
            "include_inactive": False,
            "limit": limit,
            "listing_source": "pagination",
            "owner_type": "all",
            "pivot": '{"es_pivot":"1720633844000|2746247544","page_number":1}',
            "sc_version": "1.308",
            "sort_by": "time",
            "sort_order": "desc",
            "limit_sponsored": 1,
            "user_id": "259975a4-02f7-4964-9e9c-7dbe091480d8",
            "offset": offset * limit,
        }
    )
    headers = {
        "Accept": "application/json,application/hal+json",
        "Content-Type": "application/json; charset=UTF-8",
        "Cookie": "datadome=IxKRUaZKlMeoTT3oh1aZ8vNgPEl3B6INFiVhQHNFzLbUbfaWjbPi9qYQvuIfWnBFbx7U_QhiRIQWmM_jcvbzyBq5n2cLoaFx_Gf6rpUIadWI4g9ZW1RrHz~cs7C9qYq2; didomi_token=eyJ1c2VyX2lkIjoiZTdkZDZjNjgtNjFjZS00MzM4LTk1YWQtZGU0NDgxNGNhYWFlIiwidmVuZG9ycyI6eyJlbmFibGVkIjpbImM6cm9ja3lvdSIsImM6cHVib2NlYW4tYjZCSk10c2UiLCJjOnJ0YXJnZXQtR2VmTVZ5aUMiLCJjOnNjaGlic3RlZC1NUVBYYXF5aCIsImM6Z3JlZW5ob3VzZS1RS2JHQmtzNCIsImM6cmVhbHplaXRnLWI2S0NreHlWIiwiYzpsZW1vbWVkaWEtemJZaHAyUWMiLCJjOnlvcm1lZGlhcy1xbkJXaFF5UyIsImM6bWF5dHJpY3NnLUFTMzVZYW05IiwiYzpzYW5vbWEiLCJjOnJhZHZlcnRpcy1TSnBhMjVIOCIsImM6cXdlcnRpemUtemRuZ0UyaHgiLCJjOmxiY2ZyYW5jZSIsImM6cmV2bGlmdGVyLWNScE1ucDV4IiwiYzpyZXNlYXJjaC1ub3ciLCJjOndoZW5ldmVybS04Vllod2IyUCIsImM6YWRtb3Rpb24iLCJjOnRoaXJkcHJlc2UtU3NLd21IVksiLCJjOmludG93b3dpbi1xYXp0NXRHaSIsImM6anF1ZXJ5IiwiYzpha2FtYWkiLCJjOmFiLXRhc3R5IiwiYzp6YW5veCIsImM6bW9iaWZ5IiwiYzphdC1pbnRlcm5ldCIsImM6cHVycG9zZWxhLTN3NFpmS0tEIiwiYzppbmZlY3Rpb3VzLW1lZGlhIiwiYzptYXhjZG4taVVNdE5xY0wiLCJjOmNsb3VkZmxhcmUiLCJjOmludGltYXRlLW1lcmdlciIsImM6YWR2YW5zZS1INnFiYXhuUSIsImM6c25hcGluYy15aFluSlpmVCIsImM6cmV0YXJnZXRlci1iZWFjb24iLCJjOnR1cmJvIiwiYzp0aWt0b2stS1pBVVFMWjkiLCJjOmNhYmxhdG9saS1uUm1WYXdwMiIsImM6dmlhbnQtNDd4MlloZjciLCJjOmNyZWF0ZWpzIiwiYzpicmFuY2gtVjJkRUJSeEoiLCJjOnNmci1NZHBpN2tmTiIsImM6YXBwc2ZseWVyLVlyUGRHRjYzIiwiYzpoYXNvZmZlci04WXlNVHRYaSIsImM6bGtxZC1jVTlRbUI2VyIsImM6c3dhdmVuLUxZQnJpbUFaIiwiYzpmb3J0dmlzaW9uLWllNmJYVHc5IiwiYzphZGltby1QaFVWbTZGRSIsImM6b3NjYXJvY29tLUZSY2hOZG5IIiwiYzpyZXRlbmN5LUNMZXJaaUdMIiwiYzppbGx1bWF0ZWMtQ2h0RUI0ZWsiLCJjOmFkanVzdGdtYi1wY2NOZEpCUSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzphZGxpZ2h0bmktdFdaR3JlaFQiLCJjOm02cHVibGljaS10WFRZRE5BYyIsImM6cm9ja2VyYm94LWZUTThFSjlQIiwiYzphZmZpbGluZXQiLCJjOnZ1YmxlLWNNQ0pWeDRlIl0sImRpc2FibGVkIjpbXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llcyIsImNyZWF0ZV9hZHNfcHJvZmlsZSIsInNlbGVjdF9wZXJzb25hbGl6ZWRfYWRzIiwic2VsZWN0X2Jhc2ljX2FkcyIsIm1lYXN1cmVfYWRfcGVyZm9ybWFuY2UiLCJtYXJrZXRfcmVzZWFyY2giLCJpbXByb3ZlX3Byb2R1Y3RzIiwiZ2VvbG9jYXRpb25fZGF0YSIsInVzZV9saW1pdGVkX2RhdGFfdG9fc2VsZWN0X2NvbnRlbnQiLCJleHBlcmllbmNldXRpbGlzYXRldXIiLCJtZXN1cmVhdWRpZW5jZSIsInBlcnNvbm5hbGlzYXRpb25tYXJrZXRpbmciLCJwcml4IiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdLCJkaXNhYmxlZCI6W119fQ==;__Secure-InstanceId=1a931ceb-26bc-4d38-b9e0-38c1f1ddc6c4;",
        "User-Agent": "LBC;Android;11;Android SDK built for x86;phone;a784992f815dd250;wifi;100.0.2;100000200;0",
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        timeout=5,
        proxies={"http": "http://127.0.0.1:5552", "https": "http://127.0.0.1:5552"},
        verify=False,
    )
    return response


response = get_offers(offset=0)
if response.status_code != 200:
    raise Exception(f"Error {response.status_code=}")
json_response = response.json()
max_pages = json_response["max_pages"]


offers = json_response["ads"]
for page in tqdm(range(1, max_pages + 1)):
    sleep(2)
    response = get_offers(offset=page)
    if response.status_code == 200:
        json_response = response.json()
    else:
        print(f"Error at offset {page}")
        break
    offers += json_response.get("ads", [])

print(f"{len(offers) = }")

with open("offers_v1.json", "w") as f:
    json.dump(offers, f, indent=4, ensure_ascii=False)
