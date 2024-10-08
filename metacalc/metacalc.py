# imports
import pandas as pd
import urllib.request
import json

# define url and output path
url = "https://biologicalvariation.eu/api/meta_calculations"
output_path = "out/dump.xlsx"

res = []

with urllib.request.urlopen(url) as url:
    data = json.load(url)
    print(data)

if data["code"] == "success":
    table = data["data"]

    for t in table:
        analyte = {
            "id": t["analyte"]["id"],
            "display_name": t["analyte"]["display_name"].strip(),
            "matrix": t["metas"][0]["matrix"]["matrix_expansion"] if "matrix" in t["metas"][0] else -1,
            "BV_within_median": -1,
            "BV_within_low": -1,
            "BV_within_high": -1,
            "BV_between_median": -1,
            "BV_between_low": -1,
            "BV_between_high": -1,
        }

        # cvi = within, cvg = between
        for meta in t["metas"]:
            if meta["var_type"] == ":cvi":
                analyte["BV_within_median"] = meta["median"]
                analyte["BV_within_low"] = float(meta["lower"])
                analyte["BV_within_high"] = float(meta["upper"])
            elif meta["var_type"] == ":cvg":
                analyte["BV_between_median"] = meta["median"]
                analyte["BV_between_low"] = float(meta["lower"])
                analyte["BV_between_high"] = float(meta["upper"])

        res.append(analyte)

df = pd.DataFrame.from_dict(
    res
)

# aps calculations
df["aps_bias"] = (
    0.25 * (df["BV_within_median"] ** 2 + df["BV_between_median"] ** 2) ** 0.5
)
df["aps_error"] = 1.65 * 0.5 * df["BV_within_median"] + df["aps_bias"]

# export to excel
df.to_excel(output_path, index=False)
