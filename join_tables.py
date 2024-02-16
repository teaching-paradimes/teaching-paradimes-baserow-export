import json
import os
from config import JSON_FOLDER


seed_file = os.path.join(JSON_FOLDER, "country.json")
source_file = os.path.join(JSON_FOLDER, "courses.json")

with open(seed_file, "r") as f:
    seed_data = json.load(f)

with open(source_file, "r") as f:
    source_data = json.load(f)

for key, value in source_data.items():
    old_values = value["country"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["country"] = new_values

seed_file = os.path.join(JSON_FOLDER, "university.json")
with open(seed_file, "r") as f:
    seed_data = json.load(f)

for key, value in source_data.items():
    old_values = value["university"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["university"] = new_values


with open(source_file, "w") as f:
    json.dump(source_data, f, ensure_ascii=False, indent=4)
