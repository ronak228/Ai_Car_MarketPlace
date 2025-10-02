#!/usr/bin/env python3
"""
Test script for Market Trends Analyzer
Validates all functionality and generates sample reports
"""

import sys
import os
import traceback
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from market_trends_analyzer import MarketTrendsAnalyzer
    print("✅ Successfully imported MarketTrendsAnalyzer")
except ImportError as e:
    print(f"❌ Failed to import MarketTrendsAnalyzer: {e}")
    sys.exit(1)

def test_market_analyzer():
    """Test the market trends analyzer functionality"""
    print("\n" + "="*60)
    print("🚀 TESTING MARKET TRENDS ANALYZER")
    print("="*60)
    
    try:
        # Initialize analyzer
        print("\n📊 Initializing Market Trends Analyzer...")
        analyzer = MarketTrendsAnalyzer()
        print(f"✅ Analyzer initialized successfully")
        print(f"   📈 Total records loaded: {len(analyzer.data)}")
        
        # Test market overview
        print("\n📋 Testing Market Overview...")
        overview = analyzer.get_market_overview()
        print(f"✅ Market Overview Generated")
        print(f"   🚗 Total Listings: {overview['total_listings']:,}")
        print(f"   💰 Average Price: ₹{overview['average_price']:,.2f}")
        print(f"   🏢 Total Companies: {overview['total_companies']}")
        print(f"   ⛽ Fuel Types: {len(overview['fuel_type_distribution'])}")
        
        # Test company trends
        print("\n🏢 Testing Company Trends...")
        company_trends = analyzer.get_company_trends()
        print(f"✅ Company Trends Generated")
        print(f"   📊 Companies Analyzed: {len(company_trends)}")
        
        # Show top 3 companies by market share
        top_companies = sorted(company_trends.items(), 
                             key=lambda x: x[1]['stats']['market_share'], 
                             reverse=True)[:3]
        
        print("   🏆 Top 3 Companies by Market Share:")
        for i, (company, data) in enumerate(top_companies, 1):
            print(f"      {i}. {company}: {data['stats']['market_share']:.1f}%")
        
        # Test fuel type analysis
        print("\n⛽ Testing Fuel Type Analysis...")
        fuel_analysis = analyzer.get_fuel_type_analysis()
        print(f"✅ Fuel Type Analysis Generated")
        print(f"   🔋 Fuel Types Analyzed: {len(fuel_analysis)}")
        
        for fuel, data in fuel_analysis.items():
            print(f"      {fuel}: {data['market_share']:.1f}% market share")
        
        # Test city market analysis
        print("\n🏙️ Testing City Market Analysis...")
        city_analysis = analyzer.get_city_market_analysis()
        print(f"✅ City Market Analysis Generated")
        print(f"   🌆 Cities Analyzed: {len(city_analysis)}")
        
        # Show top 3 cities by volume
        top_cities = sorted(city_analysis.items(), 
                          key=lambda x: x[1]['total_listings'], 
                          reverse=True)[:3]
        
        print("   🏆 Top 3 Cities by Listings:")
        for i, (city, data) in enumerate(top_cities, 1):
            print(f"      {i}. {city}: {data['total_listings']:,} listings")
        
        # Test price trends
        print("\n📈 Testing Price Trends...")
        price_trends = analyzer.get_price_trends_by_year()
        print(f"✅ Price Trends Generated")
        print(f"   📅 Years Analyzed: {len(price_trends)}")
        
        # Test market predictions
        print("\n🔮 Testing Market Predictions...")
        predictions = analyzer.get_market_predictions()
        print(f"✅ Market Predictions Generated")
        print(f"   📈 Trending Up: {len(predictions['trending_up'])} companies")
        print(f"   📉 Trending Down: {len(predictions['trending_down'])} companies")
        print(f"   💡 Recommendations: {len(predictions['recommendations'])}")
        
        # Test advanced analytics
        print("\n🧠 Testing Advanced Analytics...")
        analytics = analyzer.get_advanced_analytics()
        print(f"✅ Advanced Analytics Generated")
        print(f"   🔗 Correlations Analyzed: {len(analytics['correlations']['price_correlations'])}")
        print(f"   🎯 Market Segments: {len(analytics['market_segments'])}")
        
        # Show strongest correlations
        correlations = analytics['correlations']['price_correlations']
        strongest_pos = max(correlations.items(), key=lambda x: x[1])
        strongest_neg = min(correlations.items(), key=lambda x: x[1])
        
        print(f"   📊 Strongest Positive Correlation: {strongest_pos[0]} ({strongest_pos[1]:.3f})")
        print(f"   📊 Strongest Negative Correlation: {strongest_neg[0]} ({strongest_neg[1]:.3f})")
        
        # Test comprehensive report
        print("\n📄 Testing Comprehensive Report Generation...")
        report = analyzer.generate_market_report()
        print(f"✅ Comprehensive Report Generated")
        print(f"   📊 Report Timestamp: {report['timestamp']}")
        print(f"   📋 Report Sections: {len(report) - 1}")  # -1 for timestamp
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        return False

def test_api_functions():
    """Test the API utility functions"""
    print("\n" + "="*60)
    print("🌐 TESTING API UTILITY FUNCTIONS")
    print("="*60)
    
    try:
        from market_trends_analyzer import get_market_trends_data, get_company_comparison, get_price_prediction_trends
        
        # Test get_market_trends_data
        print("\n📊 Testing get_market_trends_data...")
        market_data = get_market_trends_data()
        print(f"✅ Market trends data retrieved")
        print(f"   📈 Data sections: {len(market_data)}")
        
        # Test get_company_comparison
        print("\n🏢 Testing get_company_comparison...")
        companies = ['Maruti', 'Hyundai', 'Honda']  # Common companies
        comparison = get_company_comparison(companies)
        print(f"✅ Company comparison generated")
        print(f"   🔍 Companies compared: {len(comparison)}")
        
        # Test get_price_prediction_trends with filters
        print("\n🔍 Testing get_price_prediction_trends with filters...")
        
        # Test with fuel type filter
        petrol_trends = get_price_prediction_trends(fuel_type='Petrol')
        print(f"✅ Petrol trends: Avg Price ₹{petrol_trends['average_price']:,.2f}")
        
        # Test with company filter
        maruti_trends = get_price_prediction_trends(company='Maruti')
        print(f"✅ Maruti trends: {maruti_trends['total_listings']} listings")
        
        # Test with year range filter
        recent_trends = get_price_prediction_trends(year_range=[2015, 2020])
        print(f"✅ 2015-2020 trends: Avg Price ₹{recent_trends['average_price']:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during API testing: {str(e)}")
        print(f"📍 Traceback: {traceback.format_exc()}")
        return False

def generate_sample_report():
    """Generate a sample market report"""
    print("\n" + "="*60)
    print("📄 GENERATING SAMPLE MARKET REPORT")
    print("="*60)
    
    try:
        analyzer = MarketTrendsAnalyzer()
        report = analyzer.generate_market_report()
        
        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"market_report_{timestamp}.json"
        
        import json
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✅ Sample report saved to: {filename}")
        print(f"   📊 Report size: {os.path.getsize(filename)} bytes")
        
        # Print summary
        overview = report['market_overview']
        print(f"\n📋 REPORT SUMMARY:")
        print(f"   🚗 Total Listings: {overview['total_listings']:,}")
        print(f"   💰 Market Value: ₹{overview['average_price'] * overview['total_listings']:,.0f}")
        print(f"   🏢 Companies: {overview['total_companies']}")
        print(f"   🎯 Market Segments: {len(overview['market_segments'])}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")
        return None

def main():
    """Main test function"""
    print("🚀 MARKET TRENDS ANALYZER - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test 1: Core analyzer functionality
    print("\n🧪 TEST 1: Core Analyzer Functionality")
    results.append(("Core Analyzer", test_market_analyzer()))
    
    # Test 2: API utility functions
    print("\n🧪 TEST 2: API Utility Functions")
    results.append(("API Functions", test_api_functions()))
    
    # Test 3: Sample report generation
    print("\n🧪 TEST 3: Sample Report Generation")
    report_file = generate_sample_report()
    results.append(("Report Generation", report_file is not None))
    
    # Print final results
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS")
    print("="*80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name:.<50} {status}")
        if not passed:
            all_passed = False
    
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 Market Trends Analyzer is ready for production!")
        print("   You can now run the enhanced Flask application:")
        print("   python enhanced_application.py")
    else:
        print("\n⚠️  Please fix the failing tests before proceeding.")
    
    print(f"\n⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
