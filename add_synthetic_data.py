import pandas as pd
import numpy as np
from pathlib import Path

# Config
DATA_FILE = Path(__file__).parent / 'car_data.csv'  # adjust to your dataset file
OUTPUT_FILE = Path(__file__).parent / 'car_data_synthetic_2019_2025.csv'
SEED = 42
np.random.seed(SEED)

# GST mapping (for reference in exports; model should use base price)
GST_RATES = {2019:18, 2020:20, 2021:22, 2022:25, 2023:26, 2024:28, 2025:28}


def load_dataset(path: Path) -> pd.DataFrame:
	return pd.read_csv(path)


def generate_synthetic_rows(df: pd.DataFrame) -> pd.DataFrame:
	# Expect columns at least: company, model, year, kilometers_driven, fuel_type, Price
	required = {'company','model','year','kilometers_driven','fuel_type','Price'}
	missing = required - set(df.columns)
	if missing:
		raise ValueError(f"Dataset missing required columns: {missing}")

	# Helper stats
	brand_year_stats = df.groupby(['company','year'])['Price'].median().rename('brand_year_median')
	brand_stats = df.groupby('company')['Price'].median().rename('brand_median')
	fuel_adj = df.groupby('fuel_type')['Price'].median()
	fuel_adj = (fuel_adj / fuel_adj.median()).rename('fuel_multiplier')

	df = df.merge(brand_stats, on='company', how='left')
		synthetic_rows = []
	years_target = list(range(2019, 2026))

	# Use last known brand price as baseline and apply mild yearly growth
	growth_per_year = 0.04  # 4% nominal growth baseline
	for (company, model), g in df.groupby(['company','model']):
		available_years = sorted(g['year'].unique())
		if not available_years:
			continue
		last_year = max(available_years)
		last_price = g[g['year'] == last_year]['Price'].median()
		brand_multiplier = 1.0 if np.isnan(last_price) else last_price / max(g['brand_median'].iloc[0], 1)

		for year in years_target:
			if year in available_years:
				continue
			# base price via compounded growth from last_year
			years_diff = max(0, year - last_year)
			base = last_price * ((1 + growth_per_year) ** years_diff)
			# fuel multiplier: use most common fuel for the model/brand
			fuel = g['fuel_type'].mode().iat[0] if not g['fuel_type'].mode().empty else 'Petrol'
			fm = fuel_adj.get(fuel, 1.0)
			# noise +-10%
			noise = np.random.normal(loc=0.0, scale=0.06)
			synthetic_price = max(10000, base * fm * (1 + noise))
			# kilometers: sample around median of existing for model with decay for newer years
			km_med = g['kilometers_driven'].median() if not np.isnan(g['kilometers_driven'].median()) else 50000
			km = max(0, int(km_med * (0.92 ** (year - last_year))))

			synthetic_rows.append({
				'company': company,
				'model': model,
				'year': year,
				'kilometers_driven': km,
				'fuel_type': fuel,
				'Price': round(synthetic_price, 2),
				'price_with_gst': round(synthetic_price * (1 + (GST_RATES.get(year, 18)/100.0)), 2),
				'is_synthetic': 1
			})

	return pd.DataFrame(synthetic_rows)


def main():
	if not DATA_FILE.exists():
		raise FileNotFoundError(f"Base dataset not found: {DATA_FILE}")
	base = load_dataset(DATA_FILE)
	synth = generate_synthetic_rows(base)
	synth.to_csv(OUTPUT_FILE, index=False)
	print(f"[OK] Synthetic data saved to {OUTPUT_FILE} with {len(synth)} rows")


if __name__ == '__main__':
	main()
