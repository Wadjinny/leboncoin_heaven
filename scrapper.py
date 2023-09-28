# %%
import requests
import json
from time import sleep
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")


def get_offers(offset=1, limit=30):
    url = "https://api.leboncoin.fr/finder/search"

    payload = json.dumps(
        {
            "extend": True,
            "filters": {
                "category": {"id": "10"},
                "enums": {
                    "ad_type": ["offer"],
                    # "furnished": ["1"],
                    # "real_estate_type": ["2"],
                },
                # "keywords": {"text": "appart"},
                "location": {
                    "locations": [
                        {
                            "label": "Ile-de-France",
                            "locationType": "region",
                            "region_id": "12",
                        }
                    ]
                },
                # "ranges": {
                #     # "land_plot_surface": {"max": 987, "min": 1},
                #     # "price": {"max": 987, "min": 52},
                #     # "square": {"max": 789, "min": 1},
                # },
            },
            "limit": limit,
            "limit_alu": 0,
            "limit_sponsored": 1,
            "listing_source": "direct-search",
            "offset": (offset - 1) * limit,
            # "owner_type": "private",
            "sort_by": "time",
            "sort_order": "desc",
        }
    )
    headers = {
        "Host": "api.leboncoin.fr",
        "Cookie": "__Secure-Install=63f7547a-8667-47a5-bdce-1e5d9090d3e0; __Secure-InstanceId=63f7547a-8667-47a5-bdce-1e5d9090d3e0; didomi_token=eyJ1c2VyX2lkIjoiMThhNWUwMzEtZTc4MS02NjU1LWE4MDAtZTNjNTY1Y2JiMjQ1IiwiY3JlYXRlZCI6IjIwMjMtMDktMDRUMDI6MjY6MTkuNjQ2WiIsInVwZGF0ZWQiOiIyMDIzLTA5LTA0VDAyOjI2OjE5LjY0NloiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsYmNmcmFuY2UiLCJjOnJldmxpZnRlci1jUnBNbnA1eCIsImM6ZGlkb21pIl19LCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImV4cGVyaWVuY2V1dGlsaXNhdGV1ciIsIm1lc3VyZWF1ZGllbmNlIiwicGVyc29ubmFsaXNhdGlvbm1hcmtldGluZyIsInByaXgiXX0sInZlbmRvcnNfbGkiOnsiZW5hYmxlZCI6WyJnb29nbGUiXX0sInZlcnNpb24iOjIsImFjIjoiRExXQkFBRUlBSXdBV1FCLWdHRkFQeUFra0JKWUVBd0lrZ1NrQXR5QnhBRHB3SFZnUU1BaW9CSE9DU2NFdFlLREFVSWdvdEJYT0N3VUZ0NExqQVhMQXdHQmhFREUwR1dvLkRMV0JBQUVJQUl3QVdRQi1nR0ZBUHlBa2tCSllFQXdJa2dTa0F0eUJ4QURwd0hWZ1FNQWlvQkhPQ1NjRXRZS0RBVUlnb3RCWE9Dd1VGdDRMakFYTEF3R0JoRURFMEdXbyJ9; euconsent-v2=CPxkywAPxkywAAHABBENDUCgAPLAAH7AAAAAIzNB_G_dTyPi-f59YvtwYQ1P4VQnoyACjgaNgwwJiRLBMI0EhmAIKAHqAAACIBAkICZAAQBlCAHAAAAA4IEAASMMAAAAIRAIIgCAAEAAAmJICABZC5AAAQAQgkwAABUAgAICABsgSDAAAAAAFAAAAAgAAAAAAAAAAAAAQAAAAAAAAgAAAAAAAAAAAAAEABBAEAEw1LiABsCRkJpAwiAAAjCAIAoAQAUQCQsEABASIABBGAAowAAAARQAAAAAAABAQAAAAAIAEIAAAAGBAIAAABAAAABAIBAAAAAAgAAAQAAAABADAAAAAAIACAAACAEAAIQAIACQIAAgAAAIAAAAAAAAAIBAAAAAAAAAAAAAAAAEAMUABgACCaIwADAAEE0SAAGAAIJogAAA.flgAD9gAAAAA; ry_ry-l3b0nco_realytics=eyJpZCI6InJ5X0M2OTM4MjJCLUIzMzgtNDc0Mi1BQTIxLTJDNTYyMjcxNEU3OSIsImNpZCI6bnVsbCwiZXhwIjoxNzI1MzMwMzgwMTQzLCJjcyI6bnVsbH0%3D; _gcl_au=1.1.1400186395.1693794380; panoramaId_expiry=1693880780434; include_in_experiment=true; _hjSessionUser_2783207=eyJpZCI6IjE1ZWEwYjNmLWFjYjMtNWMwMi04OTQ5LTViODk2OTkzMmRhYiIsImNyZWF0ZWQiOjE2OTM3OTQzODA3NDMsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample_2783207=1; _hjSession_2783207=eyJpZCI6IjkyMWM2ODkzLTAyZDgtNDcyOC1hNjdjLTQxNTk3MWRlZjc5MyIsImNyZWF0ZWQiOjE2OTM4NjIxNzAyMDMsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; ry_ry-l3b0nco_so_realytics=eyJpZCI6InJ5X0M2OTM4MjJCLUIzMzgtNDc0Mi1BQTIxLTJDNTYyMjcxNEU3OSIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGwsIm5zIjpmYWxzZX0%3D; cto_bundle=mwmXBF9kb0lBeDRRcXFTYU9GUVZxemZ5VGxsa2FJdXZFUXJrMncwQ1cwOXFqQXNkaFhadmVtZE9jQ2RCZFQyaDUzcWVMN1hvdko3UGt3NVRvSGF3d0w3bEVrc05ra3N6Q2haejZMNFlEZU15VUklMkZDek5mUXloUWpUTUMlMkIzaWJXRzVPejJyMUsxT2VKd09nWFUyVFVsazMlMkY2NnclM0QlM0Q; utag_main=v_id:018a5e031da3002aff551fe8c07a02074001906c00bd0$_sn:2$_ss:0$_st:1693864328498$_pn:2%3Bexp-session$ses_id:1693862169179%3Bexp-session; __gads=ID=e8f11a7c6f75dedd:T=1693794381:RT=1693862530:S=ALNI_MaT5rBKyihDMEoz48hOWybuZh9s8Q; __gpi=UID=00000c9546449c2a:T=1693794381:RT=1693862530:S=ALNI_MYwsheJsZb2Uqjl9JQGmN9NpcooHg; datadome=46p_H9pjpM-X3Td7oZ0oE-4KQgqnCRuMbPetqIc6BC~eR8VoYFJQoyBa9tTfsJiPH96VQkQmdU0ofxI4okcNG2OfizFpL9aw67wYOAMiSHXbWcQGyETBhkzu6QJYLqPa",
        "Content-Length": "347",
        "Sec-Ch-Ua": "",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Mobile": "?0",
        "Api_key": "ba0c2dad52b3ec",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36",
        "Sec-Ch-Ua-Platform": "",
        "Accept": "*/*",
        "Origin": "https://www.leboncoin.fr",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.leboncoin.fr/recherche?category=10&locations=r_12&price=1-max",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }
    ## %%
    proxies = {
        "https": "http://127.0.0.1:8080",
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        timeout=5,
        # verify=False,
        # proxies=proxies,
    )
    # response
    # # %%
    return response


# %%
response = get_offers(offset=2, limit=10)
if response.status_code != 200:
    raise Exception(f"Error {response.status_code=}")
json_response = response.json()
max_pages = json_response["max_pages"]
json_response

# %%
offers = json_response["ads"]
for offset in tqdm(range(2, max_pages + 1)):
    sleep(1)
    response = get_offers(offset=offset)
    if response.status_code == 200:
        json_response = response.json()
    else:
        print(f"Error at offset {offset}")
        break
    offers += json_response.get("ads", [])
# %%
print(f"{len(offers) = }")

# %%
with open("offers_v1.json", "w") as f:
    json.dump(offers, f, indent=4, ensure_ascii=False)
# %%
