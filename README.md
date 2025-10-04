# Maplify — Data & Reproducibility (Team Chronos)

**Project:** Maplify — Data-driven urban resilience (NASA Space Apps Challenge 2025)  
**Team:** Team Chronos (Bangladesh)  
**Lead (Data & Insights):** Rafif Kaisan Bhuiyan  

## Purpose
This repository contains the data, commands, sample inputs, and worked example needed to reproduce Maplify’s core demo outputs shown in our submission video: housing scores, flood alerts, NDVI planting zones, and commute optimizations.  

All satellite data used are open NASA products; we document product names, processing steps, and formulas.

## Folder contents
- `seed_listings.csv` / `seed_listings.json` — sample listings with component scores and MAPLIFY_SCORE.
- `data_appendix.pdf` — 1–2 page worked example showing how a single listing score was computed.
- `/layers/` — sample clipped GeoTIFF/PNG layers used in the demo.
- `/scripts/commands.txt` — GDAL & Python commands used to clip/aggregate NASA layers.
- `/scripts/compute_maplify_score.py` — example script to compute MAPLIFY_SCORE.

## Datasets used
- NASA SEDAC — GPW (population density)
- NASA VIIRS — Black Marble (nighttime lights)
- NASA MODIS — NDVI (MOD13)
- NASA MODIS — LST (MOD11)
- NASA GPM — IMERG (precipitation)
- NASA MODIS/VIIRS — AOD (aerosol optical depth)
- NASA SRTM — DEM (elevation)
- NASA POWER — climate/weather context

## MAPLIFY_SCORE (formula)
MAPLIFY_SCORE = round(
commute_score * 0.25 +
flood_score * 0.25 +
pollution_score * 0.20 +
density_score * 0.15 +
green_score * 0.15
)

Normalization examples are in `data_appendix.pdf`.

## Processing steps
1. Download NASA product tiles for your bbox.  
2. Clip with `gdalwarp -te`.  
3. Aggregate IMERG with xarray.  
4. Compute NDVI mean and LST anomaly.  
5. Compute MAPLIFY_SCORE using `compute_maplify_score.py`.  
6. Export small PNG/GeoTIFF tiles into `/layers/`.

## Limitations
- MODIS NDVI resolution 250–1000 m; Sentinel-2 recommended for validation.
- AOD→PM₂.₅ is a proxy; calibrate locally.
- IMERG thresholds vary; calibrate flood alerts locally.

## Credit & License
All satellite data and imagery: **NASA / U.S. Government**.  
This repo demonstrates usage of NASA open data. Please cite datasets on visuals (e.g., “Data: NASA GPM IMERG (2025)”).  
