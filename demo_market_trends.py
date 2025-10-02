#!/usr/bin/env python3
"""
Demo script to showcase the Advanced Market Trends functionality
"""

from datetime import datetime
import json
from market_trends_analyzer import MarketTrendsAnalyzer

def display_banner():
    """Display demo banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🚗 ADVANCED MARKET TRENDS ANALYZER - LIVE DEMO 🚗                       ║
║                                                                              ║
║    Comprehensive Car Market Intelligence & Analytics Platform                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo_market_overview(analyzer):
    """Demo market overview functionality"""
    print("\n📊 MARKET OVERVIEW ANALYSIS")
    print("=" * 60)
    
    overview = analyzer.get_market_overview()
    
    print(f"🚗 Total Market Listings: {overview['total_listings']:,}")
    print(f"💰 Average Market Price: ₹{overview['average_price']:,.2f}")
    print(f"📊 Median Market Price: ₹{overview['median_price']:,.2f}")
    print(f"🏢 Total Companies: {overview['total_companies']}")
    print(f"🚙 Total Models: {overview['total_models']}")
    print(f"📅 Average Car Age: {overview['average_age']:.1f} years")
    print(f"🛣️ Average Mileage: {overview['average_mileage']:,.0f} km")
    
    print(f"\n⛽ FUEL TYPE DISTRIBUTION:")
    for fuel, count in overview['fuel_type_distribution'].items():
        percentage = (count / overview['total_listings']) * 100
        print(f"   {fuel}: {count} vehicles ({percentage:.1f}%)")
    
    print(f"\n🏙️ TOP CITIES BY VOLUME:")
    for i, (city, count) in enumerate(list(overview['city_distribution'].items())[:5], 1):
        percentage = (count / overview['total_listings']) * 100
        print(f"   {i}. {city}: {count} listings ({percentage:.1f}%)")

def demo_company_analysis(analyzer):
    """Demo company analysis functionality"""
    print("\n\n🏢 COMPANY PERFORMANCE ANALYSIS")
    print("=" * 60)
    
    company_trends = analyzer.get_company_trends()
    
    # Sort companies by market share
    sorted_companies = sorted(company_trends.items(), 
                            key=lambda x: x[1]['stats']['market_share'], 
                            reverse=True)
    
    print("🏆 TOP 10 COMPANIES BY MARKET SHARE:")
    print("-" * 60)
    
    for i, (company, data) in enumerate(sorted_companies[:10], 1):
        stats = data['stats']
        print(f"{i:2}. {company:<15} | "
              f"Share: {stats['market_share']:5.1f}% | "
              f"Avg Price: ₹{stats['Price_mean']:8,.0f} | "
              f"Listings: {int(stats['Price_count']):4} | "
              f"Trend: {data['price_trend']:>10}")
    
    print(f"\n📈 RELIABILITY SCORES (Top 5):")
    reliability_sorted = sorted(company_trends.items(), 
                              key=lambda x: x[1]['reliability_score'], 
                              reverse=True)
    
    for i, (company, data) in enumerate(reliability_sorted[:5], 1):
        score = data['reliability_score']
        print(f"   {i}. {company}: {score:.1f}/100")

def demo_fuel_analysis(analyzer):
    """Demo fuel type analysis"""
    print("\n\n⛽ FUEL TYPE MARKET ANALYSIS")
    print("=" * 60)
    
    fuel_analysis = analyzer.get_fuel_type_analysis()
    
    for fuel_type, data in fuel_analysis.items():
        print(f"\n🔋 {fuel_type.upper()}:")
        print(f"   Market Share: {data['market_share']:.1f}%")
        print(f"   Average Price: ₹{data['average_price']:,.2f}")
        print(f"   Median Price: ₹{data['median_price']:,.2f}")
        print(f"   Average Age: {data['average_age']:.1f} years")
        print(f"   Depreciation Rate: {data['depreciation_rate']:.1f}%")
        
        print(f"   Top Companies:")
        for i, (company, count) in enumerate(list(data['popular_companies'].items())[:3], 1):
            print(f"      {i}. {company}: {count} vehicles")

def demo_city_analysis(analyzer):
    """Demo city market analysis"""
    print("\n\n🏙️ CITY MARKET ANALYSIS")
    print("=" * 60)
    
    city_analysis = analyzer.get_city_market_analysis()
    
    # Sort cities by total listings
    sorted_cities = sorted(city_analysis.items(), 
                         key=lambda x: x[1]['total_listings'], 
                         reverse=True)
    
    for i, (city, data) in enumerate(sorted_cities, 1):
        print(f"\n{i}. {city.upper()}:")
        print(f"   📊 Total Listings: {data['total_listings']:,}")
        print(f"   💰 Average Price: ₹{data['average_price']:,.2f}")
        print(f"   📈 Market Share: {data['market_share']:.1f}%")
        print(f"   🏰 Luxury Share: {data['luxury_market_share']:.1f}%")
        print(f"   💸 Budget Share: {data['budget_market_share']:.1f}%")
        
        print(f"   🏢 Top Companies:")
        for j, (company, count) in enumerate(list(data['popular_companies'].items())[:3], 1):
            print(f"      {j}. {company}: {count} vehicles")

def demo_predictions(analyzer):
    """Demo market predictions"""
    print("\n\n🔮 MARKET PREDICTIONS & INSIGHTS")
    print("=" * 60)
    
    predictions = analyzer.get_market_predictions()
    
    if predictions['trending_up']:
        print("📈 TRENDING UP COMPANIES:")
        for company_data in predictions['trending_up']:
            print(f"   🚀 {company_data['company']}: "
                  f"{company_data['market_share']:.1f}% market share, "
                  f"Reliability: {company_data['reliability_score']:.1f}/100")
    
    if predictions['trending_down']:
        print("\n📉 TRENDING DOWN COMPANIES:")
        for company_data in predictions['trending_down']:
            print(f"   📉 {company_data['company']}: "
                  f"{company_data['market_share']:.1f}% market share")
    
    if predictions['emerging_segments']:
        print("\n🌟 EMERGING MARKET SEGMENTS:")
        for segment in predictions['emerging_segments']:
            print(f"   ✨ {segment['segment']}: "
                  f"{segment['market_share']:.1f}% market share, "
                  f"Growth Potential: {segment['growth_potential']}")
    
    if predictions['recommendations']:
        print("\n💡 AI RECOMMENDATIONS:")
        for i, rec in enumerate(predictions['recommendations'], 1):
            print(f"   {i}. {rec['type']}: {rec['description']}")
            print(f"      Confidence Level: {rec['confidence']}")

def demo_advanced_analytics(analyzer):
    """Demo advanced analytics"""
    print("\n\n🧠 ADVANCED ANALYTICS")
    print("=" * 60)
    
    analytics = analyzer.get_advanced_analytics()
    
    print("🔗 PRICE CORRELATION ANALYSIS:")
    correlations = analytics['correlations']['price_correlations']
    
    # Sort by absolute correlation value
    sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    for factor, correlation in sorted_corr:
        direction = "📈 Positive" if correlation > 0 else "📉 Negative"
        strength = "Strong" if abs(correlation) > 0.5 else "Moderate" if abs(correlation) > 0.3 else "Weak"
        print(f"   {factor}: {correlation:.3f} ({direction}, {strength})")
    
    print(f"\n🎯 MARKET SEGMENTATION:")
    segments = analytics['market_segments']
    
    for segment_name, segment_data in segments.items():
        print(f"\n   {segment_name}:")
        print(f"      Size: {segment_data['size']} vehicles")
        print(f"      Avg Price: ₹{segment_data['avg_price']:,.2f}")
        print(f"      Dominant Fuel: {segment_data['dominant_fuel']}")
        print(f"      Top Company: {segment_data['dominant_company']}")
        print(f"      Profile: {segment_data['characteristics']}")

def demo_summary():
    """Display demo summary"""
    print("\n\n" + "=" * 80)
    print("🎯 DEMO SUMMARY - ADVANCED MARKET TRENDS FEATURES")
    print("=" * 80)
    
    features = [
        "✅ Comprehensive Market Overview with KPIs",
        "✅ Company Performance Analysis & Rankings",
        "✅ Fuel Type Market Distribution & Trends",
        "✅ City-wise Market Analysis & Insights",
        "✅ AI-Powered Market Predictions",
        "✅ Advanced Statistical Analytics",
        "✅ Price Correlation Analysis",
        "✅ Market Segmentation with Clustering",
        "✅ Reliability Scoring System",
        "✅ Depreciation Tracking",
        "✅ Investment Recommendations",
        "✅ RESTful API Endpoints",
        "✅ Interactive Web Dashboard",
        "✅ Real-time Data Visualization"
    ]
    
    print("\n🚀 IMPLEMENTED FEATURES:")
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n📊 API ENDPOINTS AVAILABLE:")
    endpoints = [
        "/api/market-overview",
        "/api/company-trends", 
        "/api/fuel-type-analysis",
        "/api/city-market-analysis",
        "/api/price-trends",
        "/api/market-predictions",
        "/api/advanced-analytics",
        "/api/market-report"
    ]
    
    for endpoint in endpoints:
        print(f"   🔗 http://localhost:5000{endpoint}")
    
    print(f"\n🌐 WEB INTERFACES:")
    print(f"   🏠 Main Application: http://localhost:5000")
    print(f"   📊 Market Dashboard: http://localhost:5000/market-trends")
    
    print(f"\n🎉 The Advanced Market Trends feature is fully implemented and ready!")
    print(f"   Run 'python enhanced_application.py' to start the web application.")

def main():
    """Main demo function"""
    display_banner()
    
    print(f"⏰ Demo Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔄 Initializing Market Trends Analyzer...")
    
    try:
        # Initialize analyzer
        analyzer = MarketTrendsAnalyzer()
        print("✅ Analyzer initialized successfully!")
        
        # Run all demos
        demo_market_overview(analyzer)
        demo_company_analysis(analyzer)
        demo_fuel_analysis(analyzer)
        demo_city_analysis(analyzer)
        demo_predictions(analyzer)
        demo_advanced_analytics(analyzer)
        demo_summary()
        
        print(f"\n⏰ Demo Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
