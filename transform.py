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
    entry["list_id"] = data_point.get("list_id", None)
    entry["price"] = data_point.get("price", None)[0]
    entry["subject"] = data_point.get("subject", None)
    entry["first_publication_date"] = data_point.get("first_publication_date", None)
    entry["status"] = data_point.get("status", None)
    entry["owner"] = data_point.get("owner", {}).get("type", None)
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
df.corrected_price.loc[df.corrected_price > 2000] = 2000

df.drop_duplicates(subset=["url"], inplace=True)

type_to_not_keep = ["Parking", "Autre"]
df = df[~df["real_estate_type"].isin(type_to_not_keep)]
work_pos = (45.75876540139132, 4.843617332944105)
df["distance"] = df.apply(
    lambda x: np.linalg.norm([x["lat"] - work_pos[0], x["lng"] - work_pos[1]], ord=2),
    axis=1,
)

df_dict = df.to_dict(orient="records")
with open("offers_v2.json", "w") as f:
    json.dump(df_dict, f, indent=4, ensure_ascii=False)
# %%
