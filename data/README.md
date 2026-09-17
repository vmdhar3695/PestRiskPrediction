# Data Folder

## Step 1: Get weather data (automated)
```
python fetch_weather.py --lat 16.3067 --lon 80.4365 --start 2023-01-01 --end 2024-12-31 --out weather.csv
```

## Step 2: Download pest data manually
Go to one of these (needs a free Kaggle account) and download the CSV/images into this folder:
- https://www.kaggle.com/datasets/nirmalsankalana/crop-pest-and-disease-detection
- https://www.kaggle.com/datasets/kamal01/top-agriculture-crop-disease

## Step 3: Get soil data manually
- https://soilhealth.dac.gov.in
- https://www.data.gov.in/keywords/Soil%20Health%20Card

## Step 4: Merge into one training table
Your final table should look like this (one row per crop + region + date):

| date | region | crop | temp_mean_c | humidity_pct | rain_mm | soil_n | soil_p | soil_k | soil_ph | pest_occurred |
|---|---|---|---|---|---|---|---|---|---|---|
| 2023-06-15 | Guntur | Rice | 31.2 | 78 | 12.4 | 280 | 22 | 180 | 6.8 | 1 |

`pest_occurred` (0 or 1, or a risk category) is your target/label column — this comes from your Kaggle pest dataset or historical records.

There's no code for this merge step yet because it depends on the exact shape of the pest dataset you pick — write a small pandas script once you've chosen one, matching rows by date + region as closely as your data allows.
