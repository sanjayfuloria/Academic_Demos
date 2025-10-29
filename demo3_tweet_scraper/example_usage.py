"""
Example usage of Tweet Scraper for research analysis.

This script demonstrates how to use the TweetScraper for analyzing
nonprofit and public agency communication on Twitter/X.
"""

from tweet_scraper import TweetScraper


def example_basic_usage():
    """Example 1: Basic tweet scraping and analysis."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Tweet Scraping")
    print("=" * 70)
    
    # Initialize scraper (mock mode)
    scraper = TweetScraper()
    
    # Scrape tweets from specific handles
    print("\n📡 Scraping tweets from health organizations...")
    handles = ["@WHO", "@UNICEF", "@RedCross"]
    tweets = scraper.scrape_tweets(
        handles=handles,
        max_tweets_per_handle=10,
        days_back=30
    )
    
    print(f"✓ Scraped {len(tweets)} tweets from {len(handles)} handles")
    
    # Analyze themes
    themes = scraper.analyze_themes()
    print("\n🎯 Communication Themes:")
    for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
        print(f"   {theme:20} {count:3} tweets")
    
    # Get engagement metrics
    metrics = scraper.get_engagement_metrics()
    print(f"\n💬 Engagement Metrics:")
    print(f"   Average likes per tweet:    {metrics.avg_likes:.1f}")
    print(f"   Average retweets per tweet: {metrics.avg_retweets:.1f}")
    print(f"   Total engagement rate:      {metrics.engagement_rate:.1f}")


def example_temporal_analysis():
    """Example 2: Temporal dynamics analysis."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 2: Temporal Dynamics Analysis")
    print("=" * 70)
    
    scraper = TweetScraper()
    
    # Scrape tweets from government agencies
    print("\n📡 Scraping tweets from Indian government agencies...")
    handles = ["@NITIAayog", "@MoHFW_INDIA", "@PMOIndia"]
    tweets = scraper.scrape_tweets(
        handles=handles,
        max_tweets_per_handle=15,
        days_back=14
    )
    
    print(f"✓ Scraped {len(tweets)} tweets")
    
    # Analyze by week
    print("\n📅 Weekly Analysis:")
    temporal = scraper.analyze_temporal_dynamics(interval='weekly')
    
    for week, data in sorted(temporal.items()):
        print(f"\n   Week {week}:")
        print(f"      Tweets:     {data['num_tweets']}")
        print(f"      Avg Likes:  {data['avg_likes']:.1f}")
        print(f"      Top Themes: {', '.join(data['top_themes'].keys())}")


def example_comparison_analysis():
    """Example 3: Cross-organizational comparison."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 3: Cross-Organizational Comparison")
    print("=" * 70)
    
    # Compare different sectors using separate scraper instances
    print("\n📡 Comparing Health vs Environment organizations...")
    
    health_handles = ["@WHO", "@RedCross"]
    env_handles = ["@WWF", "@Greenpeace"]
    
    # Scrape from health orgs
    health_scraper = TweetScraper()
    health_tweets = health_scraper.scrape_tweets(health_handles, max_tweets_per_handle=10)
    health_metrics = health_scraper.get_engagement_metrics()
    health_themes = health_scraper.analyze_themes()
    
    # Scrape from environment orgs
    env_scraper = TweetScraper()
    env_tweets = env_scraper.scrape_tweets(env_handles, max_tweets_per_handle=10)
    env_metrics = env_scraper.get_engagement_metrics()
    env_themes = env_scraper.analyze_themes()
    
    print("\n🏥 Health Organizations:")
    print(f"   Tweets:           {len(health_tweets)}")
    print(f"   Avg Engagement:   {health_metrics.engagement_rate:.1f}")
    print(f"   Top Theme:        {max(health_themes.items(), key=lambda x: x[1])[0]}")
    
    print("\n🌍 Environment Organizations:")
    print(f"   Tweets:           {len(env_tweets)}")
    print(f"   Avg Engagement:   {env_metrics.engagement_rate:.1f}")
    print(f"   Top Theme:        {max(env_themes.items(), key=lambda x: x[1])[0]}")


def example_data_export():
    """Example 4: Data export for further analysis."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 4: Data Export")
    print("=" * 70)
    
    scraper = TweetScraper()
    
    # Scrape comprehensive data
    print("\n📡 Scraping comprehensive dataset...")
    tweets = scraper.scrape_tweets(max_tweets_per_handle=5, days_back=7)
    print(f"✓ Scraped {len(tweets)} tweets")
    
    # Export to different formats
    print("\n💾 Exporting data...")
    
    scraper.export_to_csv("example_tweets.csv")
    print("   ✓ Exported to example_tweets.csv")
    
    scraper.export_to_json("example_tweets.json", include_analysis=True)
    print("   ✓ Exported to example_tweets.json (with analysis)")
    
    # Generate summary report
    print("\n📊 Generating summary report...")
    report = scraper.get_summary_report()
    
    with open("example_report.txt", "w") as f:
        f.write(report)
    print("   ✓ Saved summary report to example_report.txt")
    
    print("\n✅ All exports complete! Files ready for analysis.")


def example_advanced_analysis():
    """Example 5: Advanced hashtag and handle analysis."""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 5: Advanced Analysis")
    print("=" * 70)
    
    scraper = TweetScraper()
    
    # Scrape from diverse handles
    print("\n📡 Scraping tweets from diverse organizations...")
    tweets = scraper.scrape_tweets(max_tweets_per_handle=8, days_back=21)
    print(f"✓ Scraped {len(tweets)} tweets")
    
    # Top hashtags
    print("\n#️⃣  Top 10 Hashtags:")
    top_hashtags = scraper.get_top_hashtags(tweets, top_n=10)
    for i, (hashtag, count) in enumerate(top_hashtags, 1):
        print(f"   {i:2}. #{hashtag:25} {count:3} uses")
    
    # Handle statistics
    print("\n🏆 Top 5 Handles by Engagement:")
    handle_stats = scraper.get_handle_statistics()
    
    sorted_handles = sorted(
        handle_stats.items(),
        key=lambda x: x[1]['avg_likes'] + x[1]['avg_retweets'],
        reverse=True
    )[:5]
    
    for i, (handle, stats) in enumerate(sorted_handles, 1):
        avg_eng = stats['avg_likes'] + stats['avg_retweets']
        print(f"   {i}. {handle:20} Avg: {avg_eng:7.1f} ({stats['tweet_count']} tweets)")


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "Tweet Scraper - Example Usage Demonstrations" + " " * 13 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        # Run all examples
        example_basic_usage()
        example_temporal_analysis()
        example_comparison_analysis()
        example_data_export()
        example_advanced_analysis()
        
        print("\n\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
        print("\nGenerated files:")
        print("  - example_tweets.csv")
        print("  - example_tweets.json")
        print("  - example_report.txt")
        print("\nFor interactive analysis, run: streamlit run app.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
