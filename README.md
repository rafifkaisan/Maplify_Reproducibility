--

🌍 Overview

"Where NASA meets Urban Resilience, Data meets Innovation"

Cities are growing faster than ever. By 2050, nearly 70% of the world’s population will live in urban areas, creating new challenges: floods, pollution, commuting inefficiencies, and loss of green cover. NASA satellites provide detailed environmental and urban datasets, but translating these into actionable urban insights is complex.

Maplify transforms NASA open data into a city-scale decision-support tool for smarter, greener, and more resilient urban living. Our demo computes MAPLIFY_SCORES for sample neighborhoods in Dhaka, using population density, flood risk, vegetation index, pollution, and commute times.


---

⚠️ The Critical Challenge

Increasing urban population density

Rising flood & pollution risk

Poor commute & infrastructure planning

Limited accessible, actionable data for urban planners



---

🛰️ Maplify Solution

Maplify leverages NASA datasets and open-source geospatial tools to:

1. Identify flood-prone areas


2. Highlight low-green, high-density neighborhoods


3. Estimate commute efficiency


4. Generate an overall MAPLIFY_SCORE per location


5. Provide a reproducible pipeline using open-source scripts & datasets




---

📌 Repository Contents

Folder / File	Description

README.md	Project overview, reproducibility instructions
data_appendix.pdf	Worked example showing MAPLIFY_SCORE calculation
seed_listings.csv	Sample listings with input values and scores
seed_listings.json	JSON version of CSV listings
/layers/	Sample satellite layer tiles (VIIRS, IMERG, NDVI, LST)
/scripts/commands.txt	Terminal & Python commands for processing NASA layers
/scripts/compute_maplify_score.py	Python script computing MAPLIFY_SCORE from inputs



---

✨ Key Features

Satellite Data Integration

VIIRS Black Marble (nighttime lights / urban density proxy)

MODIS NDVI (green cover index)

MODIS LST (land surface temperature anomaly)

IMERG 30-day precipitation (flood proxy)

AOD (pollution proxy)

SEDAC GPW (population density)


MAPLIFY Score Computation

Normalizes all inputs to 0–100

Weighted formula:

MAPLIFY_SCORE = round(
    commute_score * 0.25 +
    flood_score   * 0.25 +
    pollution_score * 0.20 +
    density_score * 0.15 +
    green_score   * 0.15
)


Reproducibility

Fully documented pipeline (clip, aggregate, normalize, score)

Sample files in /layers/ for demonstration

Python script recomputes scores automatically


Educational / Demonstration Value

Showcases satellite-based urban analytics

Allows judges to reproduce demo in <30 minutes




---

🎨 Design & Prototype

Interactive Figma Prototype: Maplify Demo Figma
Demo Video (≤30s): YouTube Link


---

📐 Reproducible Steps

1. Download NASA data for your bounding box (VIIRS, IMERG, MODIS NDVI/LST, AOD, GPW).


2. Clip to area of interest using GDAL (gdalwarp -te <lonmin> <latmin> <lonmax> <latmax>).


3. Aggregate IMERG to 24h/30d totals using Python xarray.


4. Compute NDVI mean & LST anomalies from MODIS stacks.


5. Run MAPLIFY score script:

python scripts/compute_maplify_score.py --input seed_listings.csv --output-json seed_listings_scored.json --output-csv seed_listings_scored.csv


6. Export demo tiles for /layers/ folder.




---

📂 /layers/ Example Files

File	Description

viirs_clip.png	Sample VIIRS Black Marble tile
imerg_30d.tif	Aggregated 30-day precipitation
ndvi_mean.tif	Average NDVI raster
lst_anomaly.tif	Land surface temperature anomaly


> Use placeholders if full-resolution NASA tiles aren’t available. Judges need only sample layers for reproducibility.




---

🛠️ Scripts

scripts/commands.txt → GDAL and Python commands to process NASA layers

scripts/compute_maplify_score.py → Python 3 script to compute scores from CSV


> Make script executable: chmod +x compute_maplify_score.py




---

📚 Documentation & Data Appendix

data_appendix.pdf → Worked example: Housing Score for “Dhanmondi Studio”

Includes raw inputs, normalization, weighted computation, and interpretation

Step-by-step commands for reproducibility



---

✅ Quick Pre-Submission Checklist

[ ] README.md present and polished
[ ] data_appendix.pdf exported
[ ] seed_listings.csv / seed_listings.json present
[ ] /layers/ contains labeled sample files
[ ] /scripts/commands.txt and compute_maplify_score.py present and runnable
[ ] GitHub repo public: https://github.com/<yourusername>/Maplify_Reproducibility
[ ] Demo video uploaded (≤30s) and public
[ ] Figma prototype shared


---

⚖️ Credit & License

All satellite data: NASA / U.S. Government

This repo demonstrates usage of open NASA datasets for educational & reproducibility purpose
