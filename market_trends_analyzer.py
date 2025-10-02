"""
Advanced Market Trends Analyzer for Car Price Predictor
Provides comprehensive market analysis and trend insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from collections import defaultdict
import pickle
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

def clean_for_json(obj):
    """Clean data for JSON serialization by replacing NaN, inf, and -inf values"""
    if isinstance(obj, dict):
        return {key: clean_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        if np.isnan(obj) or np.isinf(obj):
            return 0.0
        return float(obj)
    elif pd.isna(obj):
        return None
    else:
        return obj

class MarketTrendsAnalyzer:
    def __init__(self, data_file='Cleaned_Car_data_master.csv', additional_data_file='generated_5000_strict.csv'):
        """Initialize the market trends analyzer with car data"""
        try:
            # Load main dataset
            data1 = pd.read_csv(data_file)
            print(f"✅ Main dataset loaded for analysis - {len(data1)} records")
            
            # Try to load additional dataset
            try:
                data2 = pd.read_csv(additional_data_file)
                print(f"✅ Additional dataset loaded for analysis - {len(data2)} records")
                
                # Combine both datasets
                self.data = pd.concat([data1, data2], ignore_index=True)
                print(f"✅ Combined dataset for analysis - {len(self.data)} total records")
                
            except FileNotFoundError:
                print(f"⚠️ Additional dataset not found: {additional_data_file}")
                print("Using main dataset only")
                self.data = data1
                
        except FileNotFoundError:
            print(f"❌ Main dataset not found: {data_file}")
            raise
            
        self.current_year = datetime.now().year
        self.prepare_data()
        
    def prepare_data(self):
        """Prepare and clean data for analysis"""
        # Calculate car age
        self.data['car_age'] = self.current_year - self.data['year']
        
        # Create price per km metric
        self.data['price_per_km'] = self.data['Price'] / (self.data['kms_driven'] + 1)
        
        # Create depreciation rate
        self.data['depreciation_rate'] = (self.data['predicted_price'] - self.data['Price']) / self.data['predicted_price'] * 100
        
        # Categorize price ranges
        self.data['price_category'] = pd.cut(self.data['Price'], 
                                           bins=[0, 200000, 500000, 1000000, float('inf')],
                                           labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'])
        
        # Create market segments
        self.data['market_segment'] = self.data.apply(self._categorize_segment, axis=1)
        
    def _categorize_segment(self, row):
        """Categorize cars into market segments"""
        if row['fuel_type'] == 'Electric':
            return 'Electric'
        elif row['engine_size'] > 2000:
            return 'Performance'
        elif row['Price'] > 1000000:
            return 'Luxury'
        elif row['fuel_type'] == 'Diesel' and row['Price'] > 500000:
            return 'Premium Diesel'
        elif row['car_age'] <= 3:
            return 'New/Recent'
        else:
            return 'Standard'
    
    def get_market_overview(self):
        """Get comprehensive market overview statistics"""
        overview = {
            'total_listings': len(self.data),
            'average_price': float(self.data['Price'].mean()),
            'median_price': float(self.data['Price'].median()),
            'price_std': float(self.data['Price'].std()),
            'average_age': float(self.data['car_age'].mean()),
            'average_mileage': float(self.data['kms_driven'].mean()),
            'total_companies': self.data['company'].nunique(),
            'total_models': self.data['model'].nunique(),
            'market_segments': self.data['market_segment'].value_counts().to_dict(),
            'fuel_type_distribution': self.data['fuel_type'].value_counts().to_dict(),
            'transmission_distribution': self.data['transmission'].value_counts().to_dict(),
            'city_distribution': self.data['city'].value_counts().head(10).to_dict(),
            'price_range_distribution': self.data['price_category'].value_counts().to_dict()
        }
        return clean_for_json(overview)
    
    def get_company_trends(self):
        """Analyze trends by company"""
        company_stats = self.data.groupby('company').agg({
            'Price': ['mean', 'median', 'std', 'count'],
            'car_age': 'mean',
            'kms_driven': 'mean',
            'depreciation_rate': 'mean',
            'price_per_km': 'mean'
        }).round(2)
        
        # Flatten column names
        company_stats.columns = ['_'.join(col).strip() for col in company_stats.columns]
        
        # Calculate market share
        total_listings = len(self.data)
        company_stats['market_share'] = (company_stats['Price_count'] / total_listings * 100).round(2)
        
        # Add growth indicators
        company_trends = {}
        for company in self.data['company'].unique():
            company_data = self.data[self.data['company'] == company]
            
            # Price trend analysis
            recent_cars = company_data[company_data['car_age'] <= 3]
            older_cars = company_data[company_data['car_age'] > 3]
            
            if len(recent_cars) > 0 and len(older_cars) > 0:
                price_trend = 'Increasing' if recent_cars['Price'].mean() > older_cars['Price'].mean() else 'Decreasing'
            else:
                price_trend = 'Stable'
            
            company_trends[company] = {
                'stats': company_stats.loc[company].to_dict(),
                'price_trend': price_trend,
                'popular_models': company_data['model'].value_counts().head(5).to_dict(),
                'avg_depreciation': float(company_data['depreciation_rate'].mean()),
                'reliability_score': self._calculate_reliability_score(company_data)
            }
        
        return clean_for_json(company_trends)
    
    def _calculate_reliability_score(self, company_data):
        """Calculate reliability score based on various factors"""
        score = 50  # Base score
        
        # Lower depreciation = higher reliability
        avg_depreciation = company_data['depreciation_rate'].mean()
        if avg_depreciation < -10:
            score += 20
        elif avg_depreciation < 0:
            score += 10
        elif avg_depreciation > 20:
            score -= 20
        
        # Lower accident rate = higher reliability
        accident_rate = (company_data['previous_accidents'] > 0).mean()
        if accident_rate < 0.2:
            score += 15
        elif accident_rate > 0.5:
            score -= 15
        
        # Insurance eligibility
        insurance_rate = (company_data['insurance_eligible'] == 'Yes').mean()
        score += insurance_rate * 15
        
        return max(0, min(100, score))
    
    def get_price_trends_by_year(self):
        """Analyze price trends by manufacturing year"""
        year_trends = self.data.groupby('year').agg({
            'Price': ['mean', 'median', 'count'],
            'kms_driven': 'mean',
            'depreciation_rate': 'mean'
        }).round(2)
        
        year_trends.columns = ['_'.join(col).strip() for col in year_trends.columns]
        
        # Calculate year-over-year changes
        year_trends['price_change'] = year_trends['Price_mean'].pct_change() * 100
        
        return clean_for_json(year_trends.to_dict('index'))
    
    def get_fuel_type_analysis(self):
        """Comprehensive fuel type market analysis"""
        fuel_analysis = {}
        
        for fuel_type in self.data['fuel_type'].unique():
            fuel_data = self.data[self.data['fuel_type'] == fuel_type]
            
            fuel_analysis[fuel_type] = {
                'market_share': float(len(fuel_data) / len(self.data) * 100),
                'average_price': float(fuel_data['Price'].mean()),
                'median_price': float(fuel_data['Price'].median()),
                'price_range': {
                    'min': float(fuel_data['Price'].min()),
                    'max': float(fuel_data['Price'].max())
                },
                'average_age': float(fuel_data['car_age'].mean()),
                'average_mileage': float(fuel_data['kms_driven'].mean()),
                'depreciation_rate': float(fuel_data['depreciation_rate'].mean()),
                'popular_companies': fuel_data['company'].value_counts().head(5).to_dict(),
                'city_preference': fuel_data['city'].value_counts().head(5).to_dict(),
                'maintenance_level': fuel_data['maintenance_level'].value_counts().to_dict()
            }
        
        return clean_for_json(fuel_analysis)
    
    def get_city_market_analysis(self):
        """Analyze market trends by city"""
        city_analysis = {}
        
        for city in self.data['city'].value_counts().head(10).index:
            city_data = self.data[self.data['city'] == city]
            
            city_analysis[city] = {
                'total_listings': len(city_data),
                'market_share': float(len(city_data) / len(self.data) * 100),
                'average_price': float(city_data['Price'].mean()),
                'median_price': float(city_data['Price'].median()),
                'price_std': float(city_data['Price'].std()),
                'popular_companies': city_data['company'].value_counts().head(5).to_dict(),
                'popular_fuel_types': city_data['fuel_type'].value_counts().to_dict(),
                'average_car_age': float(city_data['car_age'].mean()),
                'luxury_market_share': float(len(city_data[city_data['Price'] > 1000000]) / len(city_data) * 100),
                'budget_market_share': float(len(city_data[city_data['Price'] < 200000]) / len(city_data) * 100)
            }
        
        return clean_for_json(city_analysis)
    
    def get_market_predictions(self):
        """Generate market predictions and insights"""
        predictions = {
            'trending_up': [],
            'trending_down': [],
            'stable_markets': [],
            'emerging_segments': [],
            'recommendations': []
        }
        
        # Analyze company trends
        company_trends = self.get_company_trends()
        
        for company, data in company_trends.items():
            if data['price_trend'] == 'Increasing' and data['stats']['market_share'] > 5:
                predictions['trending_up'].append({
                    'company': company,
                    'market_share': data['stats']['market_share'],
                    'avg_price': data['stats']['Price_mean'],
                    'reliability_score': data['reliability_score']
                })
            elif data['price_trend'] == 'Decreasing':
                predictions['trending_down'].append({
                    'company': company,
                    'market_share': data['stats']['market_share'],
                    'avg_price': data['stats']['Price_mean']
                })
        
        # Identify emerging segments
        segment_growth = self.data['market_segment'].value_counts()
        for segment in segment_growth.index[:3]:
            if segment in ['Electric', 'Performance']:
                predictions['emerging_segments'].append({
                    'segment': segment,
                    'market_share': float(segment_growth[segment] / len(self.data) * 100),
                    'growth_potential': 'High'
                })
        
        # Generate recommendations
        fuel_analysis = self.get_fuel_type_analysis()
        
        if 'Electric' in fuel_analysis and fuel_analysis['Electric']['market_share'] < 5:
            predictions['recommendations'].append({
                'type': 'Investment Opportunity',
                'description': 'Electric vehicle market is emerging with high growth potential',
                'confidence': 'High'
            })
        
        if any(data['avg_depreciation'] < -5 for data in company_trends.values()):
            predictions['recommendations'].append({
                'type': 'Value Retention',
                'description': 'Some brands showing excellent value retention - good for investment',
                'confidence': 'Medium'
            })
        
        return clean_for_json(predictions)
    
    def get_advanced_analytics(self):
        """Perform advanced analytics including clustering and correlations"""
        analytics = {}
        
        # Prepare numerical data for analysis
        numerical_cols = ['Price', 'year', 'kms_driven', 'engine_size', 'power', 'car_age']
        numerical_data = self.data[numerical_cols].fillna(self.data[numerical_cols].mean())
        
        # Correlation analysis
        correlation_matrix = numerical_data.corr()
        analytics['correlations'] = {
            'price_correlations': correlation_matrix['Price'].drop('Price').to_dict(),
            'strongest_positive': correlation_matrix['Price'].drop('Price').idxmax(),
            'strongest_negative': correlation_matrix['Price'].drop('Price').idxmin()
        }
        
        # Market segmentation using clustering
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numerical_data)
        
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        self.data['cluster'] = clusters
        
        # Analyze clusters
        cluster_analysis = {}
        for cluster_id in range(5):
            cluster_data = self.data[self.data['cluster'] == cluster_id]
            cluster_analysis[f'Cluster_{cluster_id}'] = {
                'size': len(cluster_data),
                'avg_price': float(cluster_data['Price'].mean()),
                'avg_age': float(cluster_data['car_age'].mean()),
                'dominant_fuel': cluster_data['fuel_type'].mode().iloc[0] if len(cluster_data) > 0 else 'N/A',
                'dominant_company': cluster_data['company'].mode().iloc[0] if len(cluster_data) > 0 else 'N/A',
                'characteristics': self._describe_cluster(cluster_data)
            }
        
        analytics['market_segments'] = cluster_analysis
        
        # Price elasticity analysis
        analytics['price_elasticity'] = self._calculate_price_elasticity()
        
        return clean_for_json(analytics)
    
    def _describe_cluster(self, cluster_data):
        """Describe characteristics of a market cluster"""
        if len(cluster_data) == 0:
            return "Empty cluster"
        
        avg_price = cluster_data['Price'].mean()
        avg_age = cluster_data['car_age'].mean()
        
        if avg_price > 800000:
            return "Luxury segment with premium vehicles"
        elif avg_price < 200000:
            return "Budget segment with affordable options"
        elif avg_age < 3:
            return "New car segment with recent models"
        elif avg_age > 10:
            return "Vintage/Classic car segment"
        else:
            return "Mid-market segment with balanced features"
    
    def _calculate_price_elasticity(self):
        """Calculate price elasticity indicators"""
        elasticity = {}
        
        # Age vs Price elasticity
        age_price_corr = self.data['car_age'].corr(self.data['Price'])
        elasticity['age_sensitivity'] = float(abs(age_price_corr))
        
        # Mileage vs Price elasticity
        mileage_price_corr = self.data['kms_driven'].corr(self.data['Price'])
        elasticity['mileage_sensitivity'] = float(abs(mileage_price_corr))
        
        # Engine size vs Price elasticity
        engine_price_corr = self.data['engine_size'].corr(self.data['Price'])
        elasticity['engine_sensitivity'] = float(abs(engine_price_corr))
        
        return elasticity
    
    def generate_market_report(self):
        """Generate comprehensive market report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'market_overview': self.get_market_overview(),
            'company_trends': self.get_company_trends(),
            'price_trends_by_year': self.get_price_trends_by_year(),
            'fuel_type_analysis': self.get_fuel_type_analysis(),
            'city_market_analysis': self.get_city_market_analysis(),
            'market_predictions': self.get_market_predictions(),
            'advanced_analytics': self.get_advanced_analytics()
        }
        
        return clean_for_json(report)

# Utility functions for API endpoints
def get_market_trends_data():
    """Get market trends data for API consumption"""
    analyzer = MarketTrendsAnalyzer()
    return clean_for_json(analyzer.generate_market_report())

def get_company_comparison(companies):
    """Compare specific companies"""
    analyzer = MarketTrendsAnalyzer()
    company_trends = analyzer.get_company_trends()
    
    comparison = {}
    for company in companies:
        if company in company_trends:
            comparison[company] = company_trends[company]
    
    return clean_for_json(comparison)

def get_price_prediction_trends(fuel_type=None, company=None, year_range=None):
    """Get price prediction trends with filters"""
    analyzer = MarketTrendsAnalyzer()
    data = analyzer.data.copy()
    
    # Apply filters
    if fuel_type:
        data = data[data['fuel_type'] == fuel_type]
    if company:
        data = data[data['company'] == company]
    if year_range:
        data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])]
    
    # Calculate trends
    trends = {
        'average_price': float(data['Price'].mean()) if len(data) > 0 else 0,
        'median_price': float(data['Price'].median()) if len(data) > 0 else 0,
        'price_range': {
            'min': float(data['Price'].min()) if len(data) > 0 else 0,
            'max': float(data['Price'].max()) if len(data) > 0 else 0
        },
        'total_listings': len(data),
        'depreciation_trend': float(data['depreciation_rate'].mean()) if len(data) > 0 else 0
    }
    
    return clean_for_json(trends)

if __name__ == "__main__":
    # Test the analyzer
    analyzer = MarketTrendsAnalyzer()
    report = analyzer.generate_market_report()
    print("Market Trends Analysis Complete!")
    print(f"Total listings analyzed: {report['market_overview']['total_listings']}")
    print(f"Average market price: ₹{report['market_overview']['average_price']:,.2f}")
