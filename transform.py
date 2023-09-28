# %%
import json
import pandas as pd
import numpy as np

pd.options.display.max_columns = None
pd.options.plotting.backend = "plotly"
# %%
with open("offers_v1.json", "r") as f:
    data = json.load(f)
# %%


all_attr_names = [
    "charges_included",
    "district_id",
    "district_resolution_type",
    "district_type_id",
    "district_visibility",
    "elevator",
    "energy_rate",
    "floor_number",
    "furnished",
    "ges",
    "is_import",
    "lease_type",
    "nb_floors_building",
    "nb_parkings",
    "old_price",
    "outside_access",
    "profile_picture_url",
    "rating_count",
    "rating_score",
    "real_estate_type",
    "rooms",
    "square",
]


json_data = []
for data_point in data:
    entry = {}
    entry["price"] = data_point.get("price", None)[0]
    entry["subject"] = data_point.get("subject", None)
    entry["first_publication_date"] = data_point.get("first_publication_date", None)
    entry["status"] = data_point.get("status", None)
    entry["body"] = data_point.get("body", None)
    entry["has_phone"] = data_point.get("has_phone", None)
    entry["url"] = data_point.get("url", None)
    entry["lat"] = data_point.get("location", {}).get("lat", None)
    entry["lng"] = data_point.get("location", {}).get("lng", None)
    entry["city"] = data_point.get("location", {}).get("city", None)
    entry["images"] = data_point.get("images", {}).get("urls_large", None)
    if entry["images"]:
        entry["images"] = tuple(entry["images"])

    attributes = {att["key"]: att["value_label"] for att in data_point["attributes"]}
    for attr_name in all_attr_names:
        entry[attr_name] = attributes.get(attr_name, None)
    json_data.append(entry)

# %%
df = pd.DataFrame(json_data)
df["corrected_price"] = df.price
# df.corrected_price.loc[df.corrected_price > 10000] = df.corrected_price[
#     df.corrected_price > 10000
# ].apply(lambda x: x / 10 ** int(np.log10(x)) * 1000)
df.corrected_price.loc[df.corrected_price > 2000] = 2000
# %%
df.to_csv("offers_v1.csv", index=False)

# %%
