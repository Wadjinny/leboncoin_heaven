import requests
import warnings

# import pandas as pd
from time import sleep
import json
from rich import print


warnings.filterwarnings("ignore")


def get_phone_number(list_id):
    headers = {
        "Accept": "application/json,application/hal+json",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjgyYjFjNmYwLWRiM2EtNTQ2Ny1hYmI2LTJlMzAxNDViZjc3MiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiMjU5OTc1YTQtMDJmNy00OTY0LTllOWMtN2RiZTA5MTQ4MGQ4IiwiY2xpZW50X2lkIjoibGJjLWZyb250LWFuZHJvaWQiLCJkZXByZWNhdGVkX3N0b3JlX2lkIjo0MzI3OTk3MSwiZXhwIjoxNzEzODIwOTgxLCJpYXQiOjE3MTM4MTM3ODEsImluc3RhbGxfaWQiOiIxYTkzMWNlYi0yNmJjLTRkMzgtYjllMC0zOGMxZjFkZGM2YzQiLCJpc3MiOiJodHRwczovL2F1dGgubGVib25jb2luLmZyIiwianRpIjoiZTdiYmQ1ZTctMmU2Zi00Y2NiLTg1OTQtZmE3MjA5NDM3ZTY0IiwicmVmdXNlZF9zY29wZSI6IiIsInJlZnVzZWRfc2NvcGVzIjpudWxsLCJzY29wZSI6ImxiYy4qLioubWUuKiBsYmNncnAuYXV0aC5zZXNzaW9uLm1lLmRlbGV0ZSBwb2xhcmlzLiouKi5tZS4qIG9mZmxpbmUgcG9sYXJpcy4qLm1lLiogbGJjZ3JwLmF1dGgudHdvZmFjdG9yLnNtcy5tZS5hY3RpdmF0ZSBsYmNncnAuYXV0aC5zZXNzaW9uLm1lLmRpc3BsYXkgbGJjZ3JwLmF1dGgudHdvZmFjdG9yLm1lLiogbGJjLmVzY3Jvd2FjY291bnQubWFpbnRlbmFuY2UucmVhZCBsYmMuKi5tZS4qIGxiYy5wcml2YXRlIGxiY2dycC5hdXRoLnNlc3Npb24ubWUucmVhZCBsYmMuYXV0aC5lbWFpbC5wYXJ0LmNoYW5nZSBsYmNsZWdhY3kucGFydCBsYmNsZWdhY3kudXNlcnMiLCJzY29wZXMiOlsibGJjLiouKi5tZS4qIiwibGJjZ3JwLmF1dGguc2Vzc2lvbi5tZS5kZWxldGUiLCJwb2xhcmlzLiouKi5tZS4qIiwib2ZmbGluZSIsInBvbGFyaXMuKi5tZS4qIiwibGJjZ3JwLmF1dGgudHdvZmFjdG9yLnNtcy5tZS5hY3RpdmF0ZSIsImxiY2dycC5hdXRoLnNlc3Npb24ubWUuZGlzcGxheSIsImxiY2dycC5hdXRoLnR3b2ZhY3Rvci5tZS4qIiwibGJjLmVzY3Jvd2FjY291bnQubWFpbnRlbmFuY2UucmVhZCIsImxiYy4qLm1lLioiLCJsYmMucHJpdmF0ZSIsImxiY2dycC5hdXRoLnNlc3Npb24ubWUucmVhZCIsImxiYy5hdXRoLmVtYWlsLnBhcnQuY2hhbmdlIiwibGJjbGVnYWN5LnBhcnQiLCJsYmNsZWdhY3kudXNlcnMiXSwic2Vzc2lvbl9pZCI6Ijg3NzRlMGQyLWRiODktNDBiOC1hNjcwLTYzNDhkNmQ3N2E2OCIsInNpZCI6Ijg3NzRlMGQyLWRiODktNDBiOC1hNjcwLTYzNDhkNmQ3N2E2OCIsInN1YiI6ImxiYzsyNTk5NzVhNC0wMmY3LTQ5NjQtOWU5Yy03ZGJlMDkxNDgwZDg7NDMyNzk5NzEifQ.X27W6yuxz4yczz1JGNWHXC0rXTELiDLPhHXBIjEn1Fo9FBmxx11pH-nDiU2VDdmzW4dwkr2ZV79IhOmnhGwIBAC9zl9Yy15hQkRitH8AcsOSF9Yn8Dg0azCzhpWXGRqiMGsUEyJ5TkZyHQGqCtMvPmth7nRUEZ6hdYqz7yIpPhuIgQyqwkVQ9N-94BF4hJHJwU1X0OZ0Ilr4633mQMQB_PNPLH_ZnzshOhpy0vB6u7GOXRWC72JskonKZIcuRSObcZa-OjI5Cl6wIX2s0ITFV5lRttZ7GaBewnHEQpPHgG9BvdKpoeEJeQn2eIaIX7yeBBQTtpu_CzOu5bTPAY5Y8CXUecLOTh5g-oy3XEMU8nAEXQ8hlaaubNmNLtXfAk79bN7FC4Vw4voJV-azOvZYVKGZXGvh3eQMTBxx3fBkgLAcHcXbWaurkN88icY9aPxJVFnMOLgJdDBvrPMUXRja9EUpsD9ZVay7X7y4FcLxnMTcLSp077jrgoGJSDYgOF3GLkd1IFQ_QOLvMyq33cf5VNIYQBrCEDb4mw-sDmhJA4xPXLPlr_Egd9qa95tGf1kt9v1vYgrjucmv6MCKIu_h9l5iCgzke_yJSXaIAWHI-yY4yTeSZ9CAQERRiwB1UYeXiqJ5vXeIfUt6y_4F-q1GPlMQdfoulguKVszz5C__Re4",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "datadome=utazlgovAkWN3f6OEfeHiu83n~NN~mamjCeQntn01rEa0jq4SF1nxgkLq3bOIzuOl5Ha99abaesGE72pGKTbOiuH9x6UkJv0~FQvOZQN4DG7Ld5nLbDTnwGEqpW_njkc",
        "Origin": "leboncoin_android",
        "User-Agent": "LBC;Android;11;Android SDK built for x86;phone;a784992f815dd250;wifi;100.0.2;100000200;0",
    }
    body = f"app_id=leboncoin_android&list_id={list_id}&text=1"
    url = "https://api.leboncoin.fr/api/utils/phonenumber.json"
    response = requests.post(url, headers=headers, data=body)
    if not response.status_code in [200, 410]:
        print(response.text)
        raise Exception(f"Error {response.status_code=}")
    return response.json()


"""
    ['list_id','price', 'subject', 'first_publication_date', 'status', 'body',
       'has_phone', 'url', 'lat', 'lng', 'city', 'images', 'charges_included',
       'district_id', 'district_resolution_type', 'district_type_id',
       'district_visibility', 'elevator', 'owner', 'energy_rate', 'floor_number',
       'furnished', 'ges', 'is_import', 'lease_type', 'nb_floors_building',
       'nb_parkings', 'old_price', 'outside_access', 'profile_picture_url',
       'rating_count', 'rating_score', 'real_estate_type', 'rooms', 'square',
       'corrected_price', 'distance']
"""

max_dist = 0.036995
json_offers = "offers_v2_phone.json"
# json_offers = "offers_v2.json"
with open(json_offers, "r") as f:
    json_offers = json.load(f)

# print(json_offers[:2])
# exit()
from random import randint

start = 0
for i, offer in list(enumerate(json_offers))[start:]:
    if offer["distance"] <= max_dist or not offer["has_phone"]:
        continue
    while True:
        try:
            phone_number = (
                get_phone_number(offer["list_id"])
                .get("utils", {})
                .get("phonenumber", None)
            )
            break
        except Exception as e:
            print(f"Error {e=}, retrying in 60 seconds")
            sleep(60)
    print(f"{i = } {phone_number}")
    json_offers[i]["phone_number"] = phone_number

    sleep(3 + randint(1, 5))
    if i % 5 == 0:
        with open("offers_v2_phone.json", "w") as f:
            json.dump(json_offers, f, indent=4, ensure_ascii=False)
        print(f"Sleeping for 5 seconds, and saving to file")
        sleep(5)
