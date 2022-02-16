# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd

# define url and output path
url = "https://biologicalvariation.eu/meta_calculations"
output_path = "out/dump.xlsx"

# open page
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("tbody")
table_rows = table.find_all("tr")

res = []
for tr in table_rows:
    td = tr.find_all("td")
    row = [tr.text.strip() for tr in td if tr.text]
    if row:
        res.append(row)

temporary_df = pd.DataFrame(
    res,
    columns=["ID", "Marker", "Matrix", "BV", "Median", "Low", "High", "Date", "Tools"],
)

combined_rows = []

for name, rows in temporary_df.groupby("Marker"):
    _row = [rows.iloc[0, 1], rows.iloc[0, 2]] + [-1] * 6
    print(_row)
    print(len(_row))

    for row_index, row in rows.iterrows():
        if row["BV"] == "Between-subject":
            _row[5:8] = [float(x) for x in (row["Median"], row["Low"], row["High"])]
        elif row["BV"] == "Within-subject":
            _row[2:5] = [float(x) for x in (row["Median"], row["Low"], row["High"])]

    combined_rows.append(_row)

df = pd.DataFrame(
    combined_rows,
    columns=[
        "Marker",
        "Matrix",
        "BV_within_median",
        "BV_within_low",
        "BV_within_high",
        "BV_between_median",
        "BV_between_low",
        "BV_between_high",
    ],
)

# aps calculations
df["aps_bias"] = (
    0.25 * (df["BV_within_median"] ** 2 + df["BV_between_median"] ** 2) ** 0.5
)
df["aps_error"] = 1.65 * 0.5 * df["BV_within_median"] + df["aps_bias"]

# export to excel
df.to_excel(output_path, index=False)
