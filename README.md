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

MAPLIFY_SCORE = round(
    commute_score * 0.25 +
    flood_score   * 0.25 +
    pollution_score * 0.20 +
    density_score * 0.15 +
    green_score   * 0.15
)

---

## Reproducibility

- Fully documented pipeline (clip, aggregate, normalize, score)
- Sample files in /layers/ for demonstration
- Python script recomputes scores automatically

---

## Educational / Demonstration Value

- Showcases satellite-based urban analytics
- Allows judges to reproduce demo in <30 minutes

---

### 🎨 Design & Prototype

**Interactive Figma Prototype:** [https://www.figma.com/proto/cqyDQmR0e3cW0tEZN9aSk3/Untitled?node-id=1-516&t=ydsYsXawm4NT5H6u-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=1%3A516&show-proto-sidebar=1](https://www.figma.com/proto/cqyDQmR0e3cW0tEZN9aSk3/Untitled?node-id=1-516&t=ydsYsXawm4NT5H6u-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=1%3A516&show-proto-sidebar=1)

**Demo Video (≤30s):** [https://youtu.be/wSpl_mq3RM0](https://youtu.be/wSpl_mq3RM0)

---
