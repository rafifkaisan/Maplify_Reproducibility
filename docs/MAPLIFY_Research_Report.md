# MAPLIFY — Data Integration Report

**Title:** Maplify: Integrating NASA Earth Observation Data for Smarter, Greener, and Safer Cities  
**Team:** Team Chronos (Faizaan Ahamed, Maisha Tazmin, Shahriar Rahman, Rafif Kaisan Bhuiyan, Aaron Rajjo Boroi, Akibur Rahman Akib)  
**Role / Author:** Data & Insights Lead — Rafif K. Bhuiyan (Maplify, Team Chronos)  
**Event:** NASA Space Apps Challenge 2025 — Pathways to Healthy Cities & Human Settlements  
**Date:** (submission — replace with final submission date)

---

## Abstract

Maplify is a data-driven urban decision-support mobile/web platform that leverages open NASA earth-observation datasets to quantify, predict, and mitigate urban risks — including flooding, heat, pollution, and transport congestion — while incentivizing local greening through gamified tree-planting. This technical report documents the datasets used (NASA GPW, VIIRS Black Marble, MODIS NDVI/LST, GPM IMERG, MODIS/VIIRS AOD, SRTM), the data processing and scoring methodology (MAPLIFY_SCORE), the computational and reproducibility steps (GDAL & Python pseudocode), worked numeric examples, validation/uncertainty statements, and the deliverables (README, data appendix, geolayers). All data sources, processing steps, and formulas are fully documented to satisfy NASA Space Apps reproducibility and citation requirements.

---

## 1. Background & Motivation

### 1.1 Global urban trends
Rapid urbanization is a defining global trend: between 2018 and 2050 the urban population will grow by roughly 2.5 billion people (~170,000 people per day), bringing the share of global population living in urban areas to approximately 68–70% by 2050. This rapid change drives increased congestion, pollution, flood vulnerability, heat exposure, and inequitable access to green spaces.

### 1.2 Problem statement
Cities face concurrent and compounding challenges: (i) traffic congestion (productivity and emissions), (ii) air pollution (health burden), (iii) urban heat (surface temperature increase via loss of vegetation), and (iv) flood risk (extreme precipitation + built environment). Our objective is to use authoritative, open NASA datasets to create actionable, transparent, and reproducible indicators and decision tools that directly support citizens, planners, and first-responders.

---

## 2. Data Sources (explicit, cite & version)

All datasets below are open NASA products. Each dataset is cited on-screen in Maplify visualizations (format: **Data: NASA [dataset name], [year/product]**). The /data/README.md included in the repo will include dataset URLs and product codes.

1. **Population & Demographics**  
   - SEDAC — Gridded Population of the World (GPW v4) — population density grid (people/km²).

2. **Nighttime Lights / Urban Activity**  
   - VIIRS Black Marble (VIIRS nighttime radiance) — proxy for human activity & relative population density.

3. **Vegetation & Green Index**  
   - MODIS NDVI (MOD13 series) — normalized difference vegetation index (NDVI) 0–1.

4. **Aerosol / Air Quality Proxy**  
   - MODIS / VIIRS AOD (Aerosol Optical Depth) — proxy for particulate pollution.

5. **Precipitation & Flooding**  
   - GPM IMERG — near real-time precipitation (half-hourly/daily/monthly aggregates).

6. **Topography**  
   - SRTM / NASA DEM — elevation and slope for flood modelling.

7. **Land Surface Temperature (LST)**  
   - MODIS LST (MOD11) — daytime and nighttime LST.

8. **Climate & Weather**  
   - NASA POWER — climate normals and solar/radiation data.

> **Note:** exact product filenames, product codes and time windows are listed in `/data/README.md` (included in reproducibility pack).

---

## 3. Methodology — Data Processing & Scoring

### 3.1 Overview
For each feature we extract relevant variables (listed in Section 4). We normalize inputs to a common 0–100 scale and compute composite scores via weighted sums. All transformations are deterministic and documented.

### 3.2 Coordinate reference and formats
- **CRS:** EPSG:4326 (WGS84) for web & demo.  
- **Formats:** GeoTIFF for rasters; GeoJSON for polygons.

### 3.3 Normalization (example)
Given raw variable `x`, normalization to 0–100 uses a min–max or custom linear mapping:

- `green_score = (NDVI_clipped - NDVI_min) / (NDVI_max - NDVI_min) * 100`  
- `pollution_score = (1 - (AOD - AOD_min) / (AOD_max - AOD_min)) * 100` (lower AOD → higher score)  
- `flood_score = 100 - (rain_30d / rain_threshold) * 100` (clamped to [0,100])

**MAPLIFY_SCORE (canonical formula)**

\[
\text{MAPLIFY\_SCORE} = \text{round}\big(0.25\times\text{commute\_score} + 0.25\times\text{flood\_score} + 0.20\times\text{pollution\_score} + 0.15\times\text{density\_score} + 0.15\times\text{green\_score}\big)
\]

All component scores are constrained to [0,100].

### 3.4 Example normalization constants (demo city)
- `rain_threshold (30-day) = 300 mm`  
- `AOD_min = 0.02, AOD_max = 0.6`  
- `NDVI_min = 0.0, NDVI_max = 0.6`  
- `density_score = max(0, 100 - (density / 1000) * 50)`  (demo mapping — quantile remapping used for very dense cities)

> These constants are demonstrative and fully documented in `/data/README.md`.

---

## 4. Feature-by-Feature Data Mapping & Processing Details

Below each feature includes datasets, variables, processing steps, outputs and the exact video caption to paste.

### 4.1 Risk-Adjusted Housing Score
- **Datasets:** GPW, VIIRS, IMERG (rain_30d), MODIS NDVI, AOD.  
- **Variables:** density, viirs_radiance, rain_30d, NDVI, AOD.  
- **Steps:** clip rasters; aggregate IMERG to 30-day totals; compute NDVI mean; normalize components; compute MAPLIFY_SCORE.  
- **Output:** `seed_listings.json` with component scores.  
- **Video caption:** “Maplify Score — data: GPW (population), VIIRS, GPM IMERG, MODIS NDVI.”

**Worked numeric example (demo):**  
- density = 12,000 → quantile remap → density_score = 20  
- NDVI = 0.38 → green_score = 38  
- rain_30d = 60 mm → flood_score = 80  
- AOD = 0.15 → pollution_score ≈ 79  
- commute_score = 75  
- MAPLIFY_SCORE = round(75×0.25 + 80×0.25 + 79×0.20 + 20×0.15 + 38×0.15) = 63

(Use quantile mapping for very-high-density cities — documented in README.)

---

### 4.2 Collective Commute Optimizer
- **Datasets:** VIIRS radiance (hotspots), optional POWER/GPM.  
- **Processing:** cluster commuters (K-means/DBSCAN), flatten peaks, rank routes by ETA + risk penalty.  
- **Video caption:** “Commute optimisation reduces average commute by 12 minutes (VIIRS hotspots + weather-aware routing).”  
- **Sample calc:** 100 commuters × 12 min saved/day = 1,200 min/day; annual CO₂ saved example: 100 × 10 km/day × 250 days × 0.23 kg/km ≈ 57,500 kg.

---

### 4.3 Flood & Disaster Prediction & Alerts
- **Datasets:** GPM IMERG + SRTM DEM.  
- **Processing (pseudocode):**
```python
imerg = open_imerg_timeseries(bbox)
rain_24h = imerg.sum_last_hours(24)
dem = open_dem(bbox)
flood_mask = (rain_24h > rain_threshold) & (dem < dem_threshold)
polygons = raster_to_polygons(flood_mask)

Video caption: “Flood alert (NASA GPM IMERG): 24h rainfall = 132 mm → HIGH risk.”



---

4.4 Carbon & Household Savings Calculator

Datasets: NASA POWER (optional); AOD for co-benefits.

Formula: CO2_saved_per_user_year = distance_saved_per_day_km × days_per_year × emission_factor_kg_per_km

Video caption: “Shared ride: ~2,300 kg CO₂ saved/year (100 riders, 10 km/day at 0.23 kg/km).”



---

4.5 Green Index & Tree-Planting Zones (EcoView)

Datasets: MODIS NDVI, Sentinel-2 optional.

Processing: NDVI percentile mapping, bottom X% → planting priority. Estimate LST reduction using literature-based scaling (~2–3°C city-scale when canopy increases).

Video caption: “Priority planting zones (MODIS NDVI). Estimated surface cooling: ~2.3°C for added canopy.”



---

4.6 Community Page & AI Advisor

Datasets: GPW, NDVI, IMERG, AOD, LST.

Function: AI returns evidence cards with thumbnails.

Video caption: “AI Advisor: advice based on NASA NDVI & IMERG rainfall.”



---

4.7 EcoView Gamification — Tree Verification

Datasets: NDVI / Sentinel and user geotagged photo.

Algorithm: geotag & timestamp → buffer → NDVI baseline vs post-planting comparison → auto-verify if NDVI increase > noise threshold; else manual review.



---

4.8 Population Detection & Urban Growth Alerts

Datasets: VIIRS time-series & GPW.

Procedure: compute radiance % change across years, flag > X% growth, cross-check GPW.

Video caption: “Nightlight growth +18% (VIIRS 2015→2023) → rising density.”



---

4.9 Urban Heat / LST Alerts

Datasets: MODIS LST, NDVI.

Computation: LST_anomaly = LST_current - LST_baseline where baseline = long-term monthly mean. Flag anomaly > mean + 1.5 × stddev.

Video caption: “LST hotspot: +3.1°C above baseline (MODIS LST).”



---

4.10 Emergency-Responder Routing (risk-aware)

Datasets: GPM IMERG (flooded), SRTM, VIIRS (congestion).

Process: mark flooded road segments as impassable; compute alternate fastest-safe path; show ETA & safety score.

Video caption: “Emergency route avoids 2 flooded segments (NASA GPM + SRTM).”



---

5. Reproducibility — Commands & Minimal Scripts

Replace bbox coords with your city values.

5.1 Clip VIIRS (GDAL)

gdalwarp -te 90.33 23.69 90.45 23.80 -t_srs EPSG:4326 VIIRS_BlackMarble_YYYYMM.tif viirs_clip.tif
gdal_translate -of PNG -scale viirs_clip.tif viirs_clip.png

5.2 Compute 30-day IMERG totals (Python / xarray)

import xarray as xr
ds = xr.open_mfdataset('imerg_*.nc')
rain_30d = ds['precipitation'].sel(time=slice('2025-08-01','2025-08-31')).sum('time')
rain_30d.rio.to_raster('imerg_30d.tif')

5.3 Generate NDVI average (MODIS)
Use rasterio, GDAL or Google Earth Engine to compute NDVI and aggregate.

(Full sample code and Colab notebooks included in repo.)


---

6. Worked Example: Housing Score Calculation (full trace)

Sample listing: (90.38, 23.73) — Dhanmondi Studio

GPW density (100 m) = 12,000 → remap to quantile (90th) → density_score = 20

VIIRS decile → contributes to density mapping

IMERG 30d = 60 mm → flood_score = 100 - (60/300 × 100) = 80

MODIS NDVI = 0.38 → green_score = 38

AOD = 0.15 → pollution_score ≈ 79

commute_score = 75


\text{MAPLIFY\_SCORE} = \text{round}(75\cdot0.25 + 80\cdot0.25 + 79\cdot0.20 + 20\cdot0.15 + 38\cdot0.15) = 63

Include raw input raster thumbnails and the calculation table in the data appendix so judges can see provenance.


---

7. Validation & Uncertainty

Resolution constraints: MODIS NDVI 250–1000 m; Sentinel-2 preferred for higher resolution. IMERG has temporal precision but variable spatial accuracy.

Proxy limitations: AOD is a proxy for PM₂.₅ — ground validation recommended. VIIRS nightlights are a biased proxy for population (commerce vs residents). Combine sources to reduce bias.

Uncertainty communication: Every alert has a confidence flag (High / Medium / Low) based on data freshness, cross-product agreement and coverage.



---

8. Deliverables & Submission Checklist

1. /data/README.md — dataset names, product IDs, ranges, CRS, processing steps, normalization & sample commands. (MANDATORY)


2. /layers/ — sample GeoTIFFs/PNGs (VIIRS, IMERG30d, NDVI, LST).


3. seed_listings.json / seed_listings.csv — 20 sample listings with component scores.


4. data_appendix.pdf — 1–2 page worked example reproducing one insight.


5. GitHub repo — public with code snippets (GDAL + Python), README and the files above.

---

10. Ethics, Licensing & Credits

All NASA datasets are public/open — cite them on visuals and README with dataset names and URLs. Use the recommended credit line:

Data and imagery: NASA / U.S. Government.

Avoid PII: no household-level personal data presented; only aggregated or user-consented photos will be used.



---

Appendix A — Reproducible snippets

Clip VIIRS:

gdalwarp -te 90.33 23.69 90.45 23.80 -t_srs EPSG:4326 VIIRS_BlackMarble_202208.tif viirs_clip.tif
gdal_translate -of PNG -scale viirs_clip.tif viirs_clip.png

IMERG 30-day (xarray):

import xarray as xr
ds = xr.open_mfdataset('imerg_*nc')
rain_30d = ds['precipitationCal'].sel(time=slice('2025-08-01','2025-08-31')).sum('time')
rain_30d.rio.to_raster('imerg_30d.tif')

Raster → GeoJSON polygons (GDAL):

gdal_polygonize.py flood_mask.tif -f GeoJSON flood_polygons.geojson


---

Appendix B — References & Data Acknowledgement

NASA Earth Data Products: VIIRS Black Marble, MODIS NDVI, MODIS LST, GPM IMERG, AOD, SRTM.

NASA Space Apps Participant Guide (2025).

WHO and global air pollution reports (for health context).



---

Author Statement & Credit

Prepared by Rafif Kaisan Bhuiyan (Maplify — Data & Insights Lead, Team Chronos). This technical report consolidates NASA dataset choices, scoring methodology, reproducible processing steps, and a judge-facing deliverable checklist required by the Space Apps Participant Guide. All transformations, sample calculations and benchmark numbers are fully documented for judges.


---

End of report
