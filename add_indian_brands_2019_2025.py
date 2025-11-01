#!/usr/bin/env python3
"""
Augment enhanced_indian_car_dataset.csv with synthetic entries for years 2019–2025
for all Indian car brands present in the dataset.

Logic:
- Detect Indian brands by a known list and by presence in dataset.
- For each brand/model, add missing years 2019–2025 using a growth baseline,
  realistic km decay for newer years, mild randomness, and GST mapping.
- Mark new rows with is_synthetic=1 and include price_with_gst.

This script is idempotent: it only adds years missing in 2019–2025 per brand/model.
"""

import os
from typing import List, Dict
import numpy as np
import pandas as pd

PRIMARY_CANDIDATES = [
    'enhanced_indian_car_dataset.csv',
    'indian_car_brands_dataset.csv',
    'Cleaned_Car_data_master.csv'
]

# GST mapping used across the project
GST_RATES: Dict[int, int] = {2019: 18, 2020: 20, 2021: 22, 2022: 25, 2023: 26, 2024: 28, 2025: 28}

# Comprehensive list of car brands in India
# Including both Indian and international brands available in the Indian market
INDIAN_BRANDS_CANONICAL: List[str] = [
    # Indian brands
    'Maruti Suzuki', 'Maruti', 'Tata', 'Mahindra', 'Hindustan', 'Force', 'Premier',
    # International brands available in India
    'Hyundai', 'Honda', 'Toyota', 'Kia', 'MG', 'Renault', 'Nissan', 'Datsun', 
    'Volkswagen', 'Skoda', 'Ford', 'Fiat', 'Jeep', 'Citroen', 'Mercedes-Benz', 
    'BMW', 'Audi', 'Volvo', 'Jaguar', 'Land Rover', 'Lexus', 'Mini', 'Porsche',
    'Lamborghini', 'Ferrari', 'Rolls-Royce', 'Bentley', 'Aston Martin', 'Maserati',
    'Isuzu', 'Mitsubishi', 'Chevrolet', 'Opel'
]

YEARS_TARGET = list(range(2019, 2026))

# Target fuel types to ensure coverage
FUEL_TYPES_TARGET = ['Petrol', 'Diesel', 'CNG', 'LPG', 'Hybrid', 'EV']

# Baseline multipliers if dataset medians are missing
FUEL_MULT_BASE: Dict[str, float] = {
    'Petrol': 1.00,
    'Diesel': 1.05,
    'CNG': 0.92,
    'LPG': 0.90,
    'Hybrid': 1.15,
    'EV': 1.20,
}

# Kilometers driven decay factor per fuel (newer tech tends to lower kms)
KM_DECAY_FUEL: Dict[str, float] = {
    'Petrol': 0.92,
    'Diesel': 0.91,
    'CNG': 0.93,
    'LPG': 0.93,
    'Hybrid': 0.94,
    'EV': 0.95,
}


def load_dataset(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path)
    # Normalize expected column names with flexible mapping
    cols_lower = {c.lower(): c for c in df.columns}

    def ensure_col(target: str, candidates: List[str]):
        if target in df.columns:
            return
        for cand in candidates:
            if cand in df.columns:
                df.rename(columns={cand: target}, inplace=True)
                return
            # handle lower-case lookups
            if cand.lower() in cols_lower:
                df.rename(columns={cols_lower[cand.lower()]: target}, inplace=True)
                return

    # company
    ensure_col('company', ['company', 'Brand', 'brand', 'Manufacturer', 'manufacturer', 'Make', 'make'])
    # model/name
    ensure_col('model', ['model', 'Model', 'name', 'Name'])
    # year
    ensure_col('year', ['year', 'Year'])
    # kilometers driven
    ensure_col('kilometers_driven', ['kilometers_driven', 'Kilometers_Driven', 'km_driven', 'KM_Driven', 'kms_driven', 'Kms_Driven'])
    # fuel type
    ensure_col('fuel_type', ['fuel_type', 'Fuel_Type', 'fuel', 'Fuel'])
    # price
    ensure_col('Price', ['Price', 'price', 'selling_price', 'Selling_Price'])

    # If name exists but model is empty, use name
    if 'name' in df.columns and 'model' in df.columns:
        df['model'] = df['model'].fillna(df['name'])

    # Ensure required columns exist
    required = {'company', 'model', 'year', 'kilometers_driven', 'fuel_type', 'Price'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")
    return df


def find_primary_dataset() -> str:
    for candidate in PRIMARY_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    raise FileNotFoundError(
        "No primary dataset found. Expected one of: " + ", ".join(PRIMARY_CANDIDATES)
    )


def detect_indian_brands(df: pd.DataFrame) -> List[str]:
    companies = df['company'].astype(str).str.strip()
    # Match canonical names case-insensitively and allow partials
    detected = set()
    for comp in companies.unique():
        low = comp.lower()
        for canon in INDIAN_BRANDS_CANONICAL:
            if canon.lower() in low:
                detected.add(comp)
                break
    return sorted(detected)


def generate_synthetic_rows(df: pd.DataFrame, target_brands: List[str]) -> pd.DataFrame:
    np.random.seed(42)

    # Helper stats
    brand_stats = df.groupby('company')['Price'].median().rename('brand_median')
    fuel_adj = df.groupby('fuel_type')['Price'].median()
    fuel_adj = (fuel_adj / fuel_adj.median()).rename('fuel_multiplier')

    # Merge brand stats for reference
    df_ref = df.merge(brand_stats, on='company', how='left')

    synthetic_rows = []
    growth_per_year = 0.04  # 4% nominal growth baseline

    # Iterate brand/model groups restricted to Indian brands
    for (company, model), g in df_ref[df_ref['company'].isin(target_brands)].groupby(['company', 'model']):
        available_years = sorted(set(int(y) for y in g['year'].tolist() if pd.notnull(y)))
        if not available_years:
            continue

        # Use last known year and price as baseline
        last_year = max(available_years)
        last_price_series = g.loc[g['year'] == last_year, 'Price']
        last_price = float(last_price_series.median()) if not last_price_series.empty else float(g['Price'].median())
        brand_median = float(g['brand_median'].iloc[0]) if 'brand_median' in g.columns and pd.notnull(g['brand_median'].iloc[0]) else max(last_price, 1)

        # Kilometers baseline for decay (newer years fewer kms)
        km_med = g['kilometers_driven'].median() if pd.notnull(g['kilometers_driven'].median()) else 50000

        for year in YEARS_TARGET:

            # Base price via compounded growth from last_year
            years_diff = max(0, year - last_year)
            base_price = last_price * ((1 + growth_per_year) ** years_diff)

            for fuel in FUEL_TYPES_TARGET:
                # Skip creating if an entry already exists for this company/model/year/fuel
                exists_mask = (
                    (df['company'] == company) &
                    (df['model'] == model) &
                    (df['year'] == year) &
                    (df['fuel_type'].str.lower() == fuel.lower())
                )
                if exists_mask.any():
                    continue

                fuel_mult = float(fuel_adj.get(fuel, FUEL_MULT_BASE.get(fuel, 1.0)))

                # Add moderate noise per fuel
                noise = np.random.normal(loc=0.0, scale=0.06)
                price = max(10000.0, base_price * fuel_mult * (1 + noise))

                # Kilometers decay for newer years with fuel-specific factor
                decay = KM_DECAY_FUEL.get(fuel, 0.92)
                km = int(max(0, km_med * (decay ** (year - last_year))))

                # GST application (export/reference only; model uses base Price)
                gst_pct = GST_RATES.get(year, 18)
                price_with_gst = round(price * (1 + gst_pct / 100.0), 2)

                synthetic_rows.append({
                    'company': company,
                    'model': model,
                    'year': year,
                    'kilometers_driven': km,
                    'fuel_type': fuel,
                    'Price': round(price, 2),
                    'price_with_gst': price_with_gst,
                    'is_synthetic': 1
                })

    return pd.DataFrame(synthetic_rows)


def main():
    dataset_path = find_primary_dataset()
    print(f"[INFO] Loading dataset: {dataset_path}")
    df = load_dataset(dataset_path)
    indian_brands = detect_indian_brands(df)
    if not indian_brands:
        raise RuntimeError("No Indian brands detected in dataset. Please ensure brand names like 'Maruti Suzuki', 'Tata', 'Mahindra' exist.")

    print(f"[OK] Detected Indian brands ({len(indian_brands)}): {', '.join(indian_brands)}")
    synth_df = generate_synthetic_rows(df, indian_brands)
    if synth_df.empty:
        print("[INFO] No synthetic rows needed (years 2019–2025 already present).")
        return

    # Append and save
    enhanced = pd.concat([df, synth_df], ignore_index=True)
    enhanced.to_csv(dataset_path, index=False)
    print(f"[OK] Added {len(synth_df)} synthetic rows for 2019–2025 across Indian brands.")
    print(f"[STATS] New record count: {len(enhanced)} | Year range: {int(enhanced['year'].min())}-{int(enhanced['year'].max())}")


if __name__ == '__main__':
    main()