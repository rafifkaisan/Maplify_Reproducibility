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
