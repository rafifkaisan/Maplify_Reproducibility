# Maplify_Reproducibility — NASA Space Apps 2025

**Repository:** Maplify — *Smarter Cities, Greener Futures*  
**Team:** Chronos (Bangladesh)  
**Lead Data Scientist:** Rafif Kaisan Bhuiyan  

---

## 🌍 Overview

*"Where NASA meets Urban Resilience, Data meets Innovation"*

Cities are growing faster than ever. By 2050, nearly 70% of the world’s population will live in urban areas, creating challenges: floods, pollution, commuting inefficiencies, and loss of green cover. NASA satellites provide detailed environmental and urban datasets, but turning these into actionable urban insights is complex.

**Maplify** transforms NASA open data into a city-scale decision-support tool for smarter, greener, and more resilient urban living. Our demo computes **MAPLIFY_SCORES** for sample neighborhoods in Dhaka, using population density, flood risk, vegetation index, pollution, and commute times.

---

## ⚠️ The Critical Challenge

- Increasing urban population density  
- Rising flood & pollution risk  
- Poor commute & infrastructure planning  
- Limited accessible, actionable data for urban planners  

---

## 🛰️ Maplify Solution

Maplify leverages NASA datasets and open-source geospatial tools to:

1. Identify flood-prone areas  
2. Highlight low-green, high-density neighborhoods  
3. Estimate commute efficiency  
4. Generate an overall **MAPLIFY_SCORE** per location  
5. Provide a reproducible pipeline using open-source scripts & datasets  

---

## 📌 Repository Contents

| Folder / File | Description |
|---------------|------------|
| `README.md` | Project overview & reproducibility instructions |
| `data_appendix.pdf` | Worked example showing MAPLIFY_SCORE calculation |
| `seed_listings.csv` | Sample listings with input values and scores |
| `seed_listings.json` | JSON version of CSV listings |
| `/layers/` | Sample satellite layer tiles (VIIRS, IMERG, NDVI, LST) |
| `/scripts/commands.txt` | Terminal & Python commands for processing NASA layers |
| `/scripts/compute_maplify_score.py` | Python script computing MAPLIFY_SCORE from inputs |

---

## ✨ Key Features

### Satellite Data Integration

- **VIIRS Black Marble:** Nighttime lights / urban density proxy  
- **MODIS NDVI:** Green cover index  
- **MODIS LST:** Land surface temperature anomaly  
- **IMERG 30-day precipitation:** Flood proxy  
- **AOD:** Pollution proxy  
- **SEDAC GPW:** Population density  

---
## 🧮 MAPLIFY Score Computation

- **Normalizes all inputs to 0–100**  
- **Weighted formula:**

```python
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

Interactive Figma Prototype: https://www.figma.com/proto/cqyDQmR0e3cW0tEZN9aSk3/Untitled?node-id=1-516&t=ydsYsXawm4NT5H6u-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=1%3A516&show-proto-sidebar=1

Demo Video (≤30s): https://youtu.be/wSpl_mq3RM0



---

📐 Reproducible Steps

1. Download NASA data for your bounding box (VIIRS, IMERG, MODIS NDVI/LST, AOD, GPW)


2. Clip to area of interest using GDAL:



gdalwarp -te <lonmin> <latmin> <lonmax> <latmax> input.tif output_clip.tif

3. Aggregate IMERG to 24h/30d totals using Python xarray


4. Compute NDVI mean & LST anomalies from MODIS stacks


5. Run MAPLIFY score script:



python scripts/compute_maplify_score.py \
  --input seed_listings.csv \
  --output-json seed_listings_scored.json \
  --output-csv seed_listings_scored.csv

6. Export demo tiles for /layers/ folder




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


> Make script executable:



chmod +x scripts/compute_maplify_score.py


---

📚 Documentation & Data Appendix

data_appendix.md → Worked example: Housing Score for “Dhanmondi Studio”

Includes raw inputs, normalization, weighted computation, and interpretation

Step-by-step commands for reproducibility


```text
File: scripts/compute_maplify_score.py

#!/usr/bin/env python3
"""
scripts/compute_maplify_score.py

Usage:
  python scripts/compute_maplify_score.py --input seed_listings.csv --output-json seed_listings_scored.json --output-csv seed_listings_scored.csv

What this script does:
- Reads a CSV with raw variables for listings/locations.
- Normalizes each metric to a 0-100 scale (higher = better).
- Computes per-component scores:
    commute_score, flood_score, pollution_score, density_score, green_score
- Computes MAPLIFY_SCORE using default weights (override via CLI).
- Outputs scored CSV and JSON.

Expected input columns (recommended):
- id,address,lat,lon,commute_minutes,flood_mm_30d,aod,pop_density,ndvi

The script auto-detects min/max from dataset but accepts optional range overrides.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

__version__ = "1.0"

# Default column names and which direction is better (higher_is_better)
COLUMN_SPECS = {
    "commute_minutes": {"higher_is_better": False, "label": "Commute (min)"},
    "flood_mm_30d": {"higher_is_better": False, "label": "30d Precip (mm)"},
    "aod": {"higher_is_better": False, "label": "AOD (pollution)"},
    "pop_density": {"higher_is_better": False, "label": "Population density"},
    "ndvi": {"higher_is_better": True, "label": "NDVI (green index)"},
}

# Default weights
DEFAULT_WEIGHTS = {
    "commute_score": 0.25,
    "flood_score": 0.25,
    "pollution_score": 0.20,
    "density_score": 0.15,
    "green_score": 0.15,
}


def clamp(x, a=0.0, b=100.0):
    return max(a, min(b, x))


def normalize_series(series: pd.Series, higher_is_better: bool, vmin=None, vmax=None) -> pd.Series:
    """Normalize a pandas Series to 0-100 where higher_is_better=True means higher raw -> higher score."""
    # Handle NaNs by preserving them
    s = series.astype(float)
    if vmin is None:
        vmin = float(np.nanmin(s)) if not s.isna().all() else 0.0
    if vmax is None:
        vmax = float(np.nanmax(s)) if not s.isna().all() else 1.0
    if vmax == vmin:
        # constant column: assign 50 to non-NaNs
        out = pd.Series(np.where(s.isna(), np.nan, 50.0), index=s.index)
        return out
    if higher_is_better:
        out = (s - vmin) / (vmax - vmin) * 100.0
    else:
        out = (vmax - s) / (vmax - vmin) * 100.0
    out = out.clip(0.0, 100.0)
    return out


def compute_scores(df: pd.DataFrame, weights=DEFAULT_WEIGHTS, colspecs=COLUMN_SPECS, ranges=None):
    """Compute component scores and MAPLIFY score. Returns DataFrame copy with added columns."""
    dfc = df.copy()

    # Prepare ranges if provided
    ranges = ranges or {}

    # Map raw columns to normalized component names
    mapping = {
        "commute_minutes": "commute_score",
        "flood_mm_30d": "flood_score",
        "aod": "pollution_score",
        "pop_density": "density_score",
        "ndvi": "green_score",
    }

    # Normalize each column
    for raw_col, comp in mapping.items():
        if raw_col not in dfc.columns:
            dfc[comp] = np.nan
            continue
        spec = colspecs.get(raw_col, {"higher_is_better": True})
        user_range = ranges.get(raw_col)
        if user_range:
            vmin, vmax = user_range
        else:
            vmin, vmax = None, None
        dfc[comp] = normalize_series(dfc[raw_col], spec["higher_is_better"], vmin=vmin, vmax=vmax).round(3)

    # Fill missing component columns with 0 if needed
    for comp in weights.keys():
        if comp not in dfc.columns:
            dfc[comp] = 0.0

    # Compute MAPLIFY score
    dfc["_maplify_raw"] = 0.0
    for comp, w in weights.items():
        dfc["_maplify_raw"] += dfc[comp].fillna(0.0) * float(w)
    dfc["MAPLIFY_SCORE"] = dfc["_maplify_raw"].round(2)
    dfc = dfc.drop(columns=["_maplify_raw"])
    return dfc


def parse_ranges_arg(ranges_args):
    """
    Parse ranges provided as: --range commute_minutes:0:120 --range ndvi:-0.2:0.8
    Returns dict {col: (vmin, vmax)}
    """
    out = {}
    if not ranges_args:
        return out
    for r in ranges_args:
        parts = r.split(":")
        if len(parts) != 3:
            raise ValueError(f"Invalid range spec: {r}")
        col, vmin, vmax = parts
        out[col] = (float(vmin), float(vmax))
    return out


def parse_weights_arg(weights_args):
    """
    Parse weights provided as: --weight commute_score:0.25 --weight flood_score:0.25
    Returns dict mapping component -> weight. Missing components get defaults.
    """
    weights = DEFAULT_WEIGHTS.copy()
    if not weights_args:
        return weights
    for w in weights_args:
        parts = w.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid weight spec: {w}")
        comp, val = parts
        if comp not in weights:
            raise ValueError(f"Unknown component in weight spec: {comp}")
        weights[comp] = float(val)
    # normalize to sum 1 if not exactly 1
    total = sum(weights.values())
    if abs(total - 1.0) > 1e-6 and total > 0:
        weights = {k: v / total for k, v in weights.items()}
    return weights


def main(argv=None):
    p = argparse.ArgumentParser(description="Compute MAPLIFY scores from seed CSV")
    p.add_argument("--input", "-i", required=True, help="Input CSV path (seed_listings.csv)")
    p.add_argument("--output-csv", required=True, help="Output scored CSV path")
    p.add_argument("--output-json", required=False, help="Output scored JSON path")
    p.add_argument("--range", action="append", help="Override range: col:min:max (e.g. ndvi:-0.2:0.8)", default=[])
    p.add_argument("--weight", action="append", help="Override weight: comp:val (e.g. commute_score:0.25)", default=[])
    p.add_argument("--version", action="store_true")
    args = p.parse_args(argv)

    if args.version:
        print(__version__)
        sys.exit(0)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    df = pd.read_csv(str(input_path))
    # parse ranges and weights
    ranges = parse_ranges_arg(args.range)
    weights = parse_weights_arg(args.weight)

    scored = compute_scores(df, weights=weights, ranges=ranges)

    out_csv = Path(args.output_csv)
    scored.to_csv(str(out_csv), index=False)

    if args.output_json:
        out_json = Path(args.output_json)
        scored.to_json(str(out_json), orient="records", indent=2)

    # print summary
    summary = {
        "n_rows": len(scored),
        "output_csv": str(out_csv),
        "output_json": str(args.output_json) if args.output_json else None,
        "weights": weights,
        "ranges_used": ranges,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

File: scripts/commands.txt

# scripts/commands.txt
# GDAL + Python example commands used in the reproducibility pipeline

# 1) Clip a raster to bounding box (lonmin latmin lonmax latmax)
gdalwarp -t_srs EPSG:4326 -te <lonmin> <latmin> <lonmax> <latmax> input.tif output_clip.tif

# 2) Reproject and resample a raster (example)
gdalwarp -t_srs EPSG:4326 -r bilinear input.tif output_wgs84.tif

# 3) Build a VRT (stack) from many MODIS tiles, then compute mean with gdal_calc
gdalbuildvrt modis_stack.vrt modis_tile_*.tif
gdal_translate -of GTiff modis_stack.vrt modis_stack.tif
# compute mean via gdal_calc (example, uses numpy operations)
gdal_calc.py -A modis_stack.tif --outfile=ndvi_mean.tif --calc="A" --NoDataValue=-9999

# 4) Aggregate IMERG netCDF to 24h or 30-day totals (using xarray in Python)
# See example Python snippet below (save as scripts/aggregate_imerg.py or run interactively)

"""
python - <<'PY'
import xarray as xr
ds = xr.open_dataset('IMERG_file.nc')   # adapt filename
# assume precipitation variable is 'precipitation' or 'precip'
precip = ds['precipitation']  # change if needed
# resample to daily
daily = precip.resample(time='1D').sum(dim='time')
# save daily to netcdf
daily.to_netcdf('imerg_daily.nc')
# for 30-day rolling sum
rolling_30 = daily.rolling(time=30, min_periods=1).sum()
rolling_30.to_netcdf('imerg_30d.nc')
PY
"""

# 5) Example xarray snippet to compute NDVI mean from many GeoTiffs (using rioxarray)
"""
python - <<'PY'
import rioxarray as rxr
import xarray as xr
import glob
files = sorted(glob.glob('ndvi_tiles/*.tif'))
stack = xr.concat([rxr.open_rasterio(f).squeeze() for f in files], dim='time')
ndvi_mean = stack.mean(dim='time')
ndvi_mean.rio.to_raster('ndvi_mean.tif')
PY
"""

# 6) Example: Run MAPLIFY score script (from repo root)
python3 scripts/compute_maplify_score.py \
  --input seed_listings.csv \
  --output-csv seed_listings_scored.csv \
  --output-json seed_listings_scored.json

# 7) Make script executable
chmod +x scripts/compute_maplify_score.py

File: seed_listings.csv

id,address,lat,lon,commute_minutes,flood_mm_30d,aod,pop_density,ndvi
1,"Dhanmondi Studio, Dhaka",23.7465,90.3745,18,12,0.48,23000,0.26
2,"Gulshan Apartment, Dhaka",23.7925,90.4076,35,5,0.35,15000,0.12
3,"Mirpur Flat, Dhaka",23.8065,90.3652,45,40,0.55,40000,0.05
4,"Uttara House, Dhaka",23.8756,90.3980,25,2,0.30,8000,0.30
5,"Old Dhaka, Dhaka",23.7286,90.3940,50,80,0.70,52000,0.02

File: layers/README.md

# /layers/ — Example satellite layer placeholders

Place sample (small) files here for judges to check reproducibility quickly.

Expected example files (placeholders ok):
- `viirs_clip.png` — reduced-resolution PNG showing VIIRS Black Marble tile for AOI
- `imerg_30d.tif` — aggregated 30-day precipitation GeoTIFF (small subset or clipped)
- `ndvi_mean.tif` — mean NDVI GeoTIFF (clipped to AOI)
- `lst_anomaly.tif` — land surface temperature anomaly GeoTIFF (clipped)

Notes:
- Use small, low-resolution placeholder files if full-size datasets are too large.
- Filenames should match the README references above.

File: data_appendix.md

# data_appendix.md

Worked example: Housing Score for "Dhanmondi Studio"

## Raw inputs (row id=1 from seed_listings.csv)
- commute_minutes: 18
- flood_mm_30d: 12
- aod: 0.48
- pop_density: 23000
- ndvi: 0.26

## Normalization (using dataset min/max from seed_listings.csv)
- commute_score (lower commute is better): normalized to 0-100
- flood_score (lower flood is better): normalized to 0-100
- pollution_score (AOD lower is better): normalized to 0-100
- density_score (lower population density is better): normalized to 0-100
- green_score (higher NDVI is better): normalized to 0-100

## Weighted computation
MAPLIFY_SCORE = round(
    commute_score * 0.25 +
    flood_score   * 0.25 +
    pollution_score * 0.20 +
    density_score * 0.15 +
    green_score   * 0.15
)

## Interpretation
Higher MAPLIFY_SCORE => better overall urban livability according to our composite metric.

File: .gitignore

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
env/
.env

# Data
*.tif
*.nc
*.hdf
*.sqlite
*.db

# Outputs
*scored.csv
*scored.json

File: LICENSE

MIT License

Copyright (c) 2025 Team Chronos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

File: usage_examples.sh

#!/usr/bin/env bash
# Small convenience script showing typical run commands

# 1) Make python script executable
chmod +x scripts/compute_maplify_score.py

# 2) Run scoring using default auto-ranges (computed from CSV)
python3 scripts/compute_maplify_score.py \
  --input seed_listings.csv \
  --output-csv seed_listings_scored.csv \
  --output-json seed_listings_scored.json

# 3) Run scoring with explicit ranges (example)
python3 scripts/compute_maplify_score.py \
  --input seed_listings.csv \
  --output-csv seed_listings_scored_ranges.csv \
  --output-json seed_listings_scored_ranges.json \
  --range commute_minutes:0:120 \
  --range flood_mm_30d:0:200 \
  --range aod:0:1 \
  --range pop_density:0:60000 \
  --range ndvi:-0.2:0.8

# 4) Run scoring with custom weights
python3 scripts/compute_maplify_score.py \
  --input seed_listings.csv \
  --output-csv seed_listings_scored_custom_weights.csv \
  --weight commute_score:0.20 \
  --weight flood_score:0.30 \
  --weight pollution_score:0.20 \
  --weight density_score:0.15 \
  --weight green_score:0.15

File: CONTRIBUTING.md

# Contributing

- Open issues for bugs / enhancements.
- Submit PRs with clear descriptions and tests where applicable.
- Keep data files small for repository; store large raw satellite files externally and provide links.
