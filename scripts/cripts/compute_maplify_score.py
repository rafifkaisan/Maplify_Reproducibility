#!/usr/bin/env python3
"""
compute_maplify_score.py
Reads seed_listings.csv and (re)computes MAPLIFY_SCORE for each row.
Writes JSON output (maplify_scored.json) and updated CSV (seed_listings_scored.csv).
"""
import csv, json, argparse, math

def clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))

def compute_commute_score(commute_mins):
    # commute_mins: travel duration in minutes (lower is better)
    # baseline: 10 mins -> 100; each extra minute loses 2 points
    score = 100.0 - max(0.0, (commute_mins - 10.0)) * 2.0
    return clamp(score)

def compute_flood_score(flood_zone):
    # flood_zone: integer 0 (best) .. 3 (worst) in demo
    try:
        zone = float(flood_zone)
    except:
        zone = 3.0
    score = ((3.0 - zone) / 3.0) * 100.0
    return clamp(score)

def compute_pollution_score(aod, aod_min=0.02, aod_max=0.6):
    try:
        a = float(aod)
    except:
        a = aod_max
    score = (1.0 - (a - aod_min) / (aod_max - aod_min)) * 100.0
    return clamp(score)

def compute_density_score(density, max_density=40000.0):
    try:
        d = float(density)
    except:
        d = max_density
    score = 100.0 - (d / max_density) * 100.0
    return clamp(score)

def compute_green_score(ndvi, ndvi_min=0.0, ndvi_max=0.6):
    try:
        n = float(ndvi)
    except:
        n = ndvi_min
    # scale NDVI [min,max] to 0-100
    score = (n - ndvi_min) / (ndvi_max - ndvi_min) * 100.0
    return clamp(score)

def compute_maplify_score(commute_score, flood_score, pollution_score, density_score, green_score):
    s = commute_score * 0.25 + flood_score * 0.25 + pollution_score * 0.20 + density_score * 0.15 + green_score * 0.15
    return int(round(s))

def main(infile, outjson, outcsv):
    rows_out = []
    with open(infile, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        fieldnames = r.fieldnames if r.fieldnames else []
        for row in r:
            # compute or use provided component scores
            commute_mins = float(row.get('commute_mins') or 0)
            flood_zone = row.get('flood_zone') or 3
            aod = row.get('aod') or 0.6
            ndvi = row.get('ndvi') or 0.0
            density = row.get('density_per_km2') or 40000

            commute_score = float(row.get('commute_score') or compute_commute_score(commute_mins))
            flood_score = float(row.get('flood_score') or compute_flood_score(flood_zone))
            pollution_score = float(row.get('pollution_score') or compute_pollution_score(aod))
            density_score = float(row.get('density_score') or compute_density_score(density))
            green_score = float(row.get('green_score') or compute_green_score(ndvi))

            maplify_score = compute_maplify_score(commute_score, flood_score, pollution_score, density_score, green_score)

            # add/overwrite computed fields
            row['commute_score'] = round(commute_score, 2)
            row['flood_score'] = round(flood_score, 2)
            row['pollution_score'] = round(pollution_score, 2)
            row['density_score'] = round(density_score, 2)
            row['green_score'] = round(green_score, 2)
            row['maplify_score'] = maplify_score

            rows_out.append(row)

    # write JSON
    with open(outjson, 'w', encoding='utf-8') as f:
        json.dump(rows_out, f, indent=2, ensure_ascii=False)

    # write CSV
    out_fields = list(rows_out[0].keys()) if rows_out else fieldnames
    with open(outcsv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    print("Wrote", outjson, "and", outcsv)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute MAPLIFY scores from CSV')
    parser.add_argument('--input', default='seed_listings.csv', help='input CSV')
    parser.add_argument('--output-json', default='seed_listings_scored.json', help='output JSON')
    parser.add_argument('--output-csv', default='seed_listings_scored.csv', help='output CSV')
    args = parser.parse_args()
    main(args.input, args.output_json, args.output_csv)
