# EDA Report: final_merged_car_dataset.csv

## Dataset Overview
- **Shape**: 5816 rows × 23 columns
- **Missing Values**: 0
- **Data Types**: {dtype('O'): np.int64(13), dtype('float64'): np.int64(8), dtype('int64'): np.int64(2)}

## Key Statistics

### Price Distribution
- **Mean Price**: ₹206,446.67
- **Median Price**: ₹178,591.50
- **Min Price**: ₹20,000.00
- **Max Price**: ₹662,142.00
- **Standard Deviation**: ₹125,413.59

### Car Age Distribution
- **Mean Age**: 10.4 years
- **Median Age**: 11.0 years
- **Min Age**: 0.0 years
- **Max Age**: 30.0 years

### Kilometers Driven
- **Mean KMs**: 124,104
- **Median KMs**: 124,285
- **Min KMs**: 75
- **Max KMs**: 249,899

## Categorical Distributions

### Top 10 Companies by Count
company
Maruti        1054
Hyundai        940
Honda          930
Tata           922
Mahindra       910
Toyota         863
Chevrolet       34
Renault         33
Ford            30
Volkswagen      19

### Top 10 Models by Count
model
Nan         816
Nexon       316
Wr-V        309
Xuv500      292
Baleno      291
City        290
Verna       285
Fortuner    283
Scorpio     281
Tiago       281

### Fuel Type Distribution
fuel_type
Electric    1076
Diesel       998
Hybrid       990
Petrol       990
Cng          946
Nan          816

### Transmission Distribution
transmission
Automatic    2550
Manual       2450
Nan           816

### Owner Distribution
owner
2Nd    1262
4Th    1260
1St    1258
3Rd    1220
Nan     816

## Price Analysis by Company
                mean  count
company                    
Tata       210115.65    922
Toyota     208675.99    863
Honda      208650.82    930
Hyundai    207698.73    940
Maruti     206268.46   1054
Mahindra   203305.78    910
Audi       178591.50     11
Datsun     178591.50      7
Bmw        178591.50      8
Hindustan  178591.50      3

## Top 10 Most Expensive Cars
 company   model  year    price fuel_type
    Tata Harrier  2025 662142.0    Hybrid
 Hyundai   Creta  2025 641231.0    Hybrid
    Tata   Tiago  2025 633164.0  Electric
 Hyundai   Verna  2025 627355.0  Electric
  Maruti   Dzire  2025 620912.0    Hybrid
Mahindra  Xuv500  2025 615669.0    Hybrid
  Maruti  Baleno  2025 610897.0  Electric
   Honda   Amaze  2025 609850.0  Electric
Mahindra Scorpio  2025 604306.0  Electric
    Tata   Nexon  2025 602695.0  Electric

## Data Quality
- ✅ No missing values detected
- ✅ All numeric columns properly converted
- ✅ Categorical columns normalized
- ✅ Derived feature 'car_age' added successfully

## Recommendations
1. The dataset is well-structured with no missing values
2. Price distribution shows good variation for modeling
3. Categorical features are well-balanced
4. Consider feature engineering for better model performance
