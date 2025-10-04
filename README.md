# Maplify_Reproducibility — NASA Space Apps 2025

**Repository:** Maplify — *Smarter Cities, Greener Futures*  
**Team:** Team Chronos (Bangladesh)  
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

#!/usr/bin/env python3
"""
Maplify Score Computation Script
Author: Rafif Kaisan Bhuiyan
Team: Team Chronos
Purpose: Compute MAPLIFY_SCORE for sample neighborhoods using CSV/JSON inputs.
"""

import pandas as pd
import json
import argparse

def compute_maplify_score(row):
    """
    Compute the MAPLIFY_SCORE using weighted formula.
    Inputs are assumed to be normalized 0-100.
    """
    return round(
        row['commute_score'] * 0.25 +
        row['flood_score'] * 0.25 +
        row['pollution_score'] * 0.20 +
        row['density_score'] * 0.15 +
        row['green_score'] * 0.15
    )

def load_csv(file_path):
    """Load CSV file into pandas DataFrame"""
    return pd.read_csv(file_path)

def save_csv(df, file_path):
    """Save pandas DataFrame to CSV"""
    df.to_csv(file_path, index=False)

def save_json(df, file_path):
    """Save pandas DataFrame to JSON"""
    df.to_json(file_path, orient='records', indent=4)

def main(input_csv, output_csv, output_json):
    # Load input CSV
    df = load_csv(input_csv)

    # Check required columns exist
    required_cols = ['commute_score', 'flood_score', 'pollution_score', 'density_score', 'green_score']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Compute MAPLIFY_SCORE for each row
    df['MAPLIFY_SCORE'] = df.apply(compute_maplify_score, axis=1)

    # Save outputs
    save_csv(df, output_csv)
    save_json(df, output_json)

    print(f"✅ MAPLIFY_SCORE computed and saved to:\n  CSV: {output_csv}\n  JSON: {output_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute MAPLIFY_SCORE for input CSV.")
    parser.add_argument("--input", required=True, help="Input CSV file with scores")
    parser.add_argument("--output-csv", required=True, help="Output CSV file with MAPLIFY_SCORE")
    parser.add_argument("--output-json", required=True, help="Output JSON file with MAPLIFY_SCORE")

    args = parser.parse_args()
    main(args.input, args.output_csv, args.output_json)
