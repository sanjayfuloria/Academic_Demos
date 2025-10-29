"""
Unit tests for Tweet Scraper module.
"""

import unittest
import os
import json
import csv
from datetime import datetime, timedelta
from tweet_scraper import TweetScraper, Tweet, EngagementMetrics


class TestTweetScraper(unittest.TestCase):
    """Test cases for TweetScraper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = TweetScraper()
        
        # Create sample tweets for testing
        self.sample_tweets = [
            Tweet(
                tweet_id="1001",
                handle="@UNICEF",
                text="Vaccination campaign reaches 5 million children. #Health #Vaccine",
                created_at=datetime.now().isoformat(),
                likes=500,
                retweets=150,
                replies=50,
                hashtags=["Health", "Vaccine"],
                mentions=[],
                url="https://twitter.com/UNICEF/status/1001"
            ),
            Tweet(
                tweet_id="1002",
                handle="@WHO",
                text="Climate change affects public health. #Environment #ClimateAction",
                created_at=(datetime.now() - timedelta(days=1)).isoformat(),
                likes=800,
                retweets=200,
                replies=75,
                hashtags=["Environment", "ClimateAction"],
                mentions=[],
                url="https://twitter.com/WHO/status/1002"
            ),
            Tweet(
                tweet_id="1003",
                handle="@WWF",
                text="Conservation efforts protect wildlife habitats. #Wildlife #Conservation",
                created_at=(datetime.now() - timedelta(days=2)).isoformat(),
                likes=600,
                retweets=180,
                replies=60,
                hashtags=["Wildlife", "Conservation"],
                mentions=[],
                url="https://twitter.com/WWF/status/1003"
            )
        ]
    
    def tearDown(self):
        """Clean up test files."""
        test_files = ['test_tweets.csv', 'test_tweets.json']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_initialization(self):
        """Test TweetScraper initialization."""
        scraper = TweetScraper()
        self.assertIsNotNone(scraper)
        self.assertTrue(scraper.mock_mode)
        self.assertEqual(len(scraper.tweets), 0)
        
    def test_verified_handles_list(self):
        """Test that verified handles list is properly configured."""
        self.assertIsInstance(self.scraper.VERIFIED_HANDLES, list)
        self.assertGreater(len(self.scraper.VERIFIED_HANDLES), 20)
        self.assertLess(len(self.scraper.VERIFIED_HANDLES), 50)
        
        # Check some expected handles are present
        expected_handles = ["@UNICEF", "@WHO", "@WWF", "@NITIAayog", "@MoHFW_INDIA"]
        for handle in expected_handles:
            self.assertIn(handle, self.scraper.VERIFIED_HANDLES)
    
    def test_communication_themes(self):
        """Test that communication themes are properly defined."""
        themes = self.scraper.COMMUNICATION_THEMES
        self.assertIsInstance(themes, dict)
        
        # Check expected themes
        expected_themes = ['health', 'education', 'environment', 'disaster', 
                          'development', 'social_welfare', 'humanitarian', 'technology']
        for theme in expected_themes:
            self.assertIn(theme, themes)
            self.assertIsInstance(themes[theme], list)
            self.assertGreater(len(themes[theme]), 0)
    
    def test_scrape_tweets_mock_mode(self):
        """Test tweet scraping in mock mode."""
        tweets = self.scraper.scrape_tweets(handles=["@UNICEF", "@WHO"], 
                                           max_tweets_per_handle=10,
                                           days_back=7)
        
        self.assertIsInstance(tweets, list)
        self.assertGreater(len(tweets), 0)
        
        # Verify tweet structure
        for tweet in tweets:
            self.assertIsInstance(tweet, Tweet)
            self.assertIsInstance(tweet.tweet_id, str)
            self.assertIsInstance(tweet.handle, str)
            self.assertIsInstance(tweet.text, str)
            self.assertIsInstance(tweet.likes, int)
            self.assertIsInstance(tweet.retweets, int)
            self.assertIsInstance(tweet.replies, int)
            self.assertIsInstance(tweet.hashtags, list)
            self.assertIsInstance(tweet.mentions, list)
    
    def test_analyze_themes(self):
        """Test theme analysis functionality."""
        themes = self.scraper.analyze_themes(self.sample_tweets)
        
        self.assertIsInstance(themes, dict)
        self.assertGreater(len(themes), 0)
        
        # Verify themes were detected
        self.assertIn('health', themes)
        self.assertIn('environment', themes)
        
        # Verify counts
        total_count = sum(themes.values())
        self.assertEqual(total_count, len(self.sample_tweets))
    
    def test_get_engagement_metrics(self):
        """Test engagement metrics calculation."""
        metrics = self.scraper.get_engagement_metrics(self.sample_tweets)
        
        self.assertIsInstance(metrics, EngagementMetrics)
        
        # Verify calculated values
        self.assertEqual(metrics.total_likes, 500 + 800 + 600)
        self.assertEqual(metrics.total_retweets, 150 + 200 + 180)
        self.assertEqual(metrics.total_replies, 50 + 75 + 60)
        
        # Verify averages
        self.assertAlmostEqual(metrics.avg_likes, 1900 / 3, places=1)
        self.assertAlmostEqual(metrics.avg_retweets, 530 / 3, places=1)
        self.assertAlmostEqual(metrics.avg_replies, 185 / 3, places=1)
        
        # Verify engagement rate
        expected_rate = (1900 + 530 + 185) / 3
        self.assertAlmostEqual(metrics.engagement_rate, expected_rate, places=1)
    
    def test_get_engagement_metrics_empty(self):
        """Test engagement metrics with empty tweet list."""
        metrics = self.scraper.get_engagement_metrics([])
        
        self.assertEqual(metrics.total_likes, 0)
        self.assertEqual(metrics.total_retweets, 0)
        self.assertEqual(metrics.total_replies, 0)
        self.assertEqual(metrics.avg_likes, 0.0)
    
    def test_analyze_temporal_dynamics(self):
        """Test temporal dynamics analysis."""
        temporal = self.scraper.analyze_temporal_dynamics(self.sample_tweets, 
                                                         interval='daily')
        
        self.assertIsInstance(temporal, dict)
        self.assertGreater(len(temporal), 0)
        
        # Verify structure of temporal data
        for date_key, data in temporal.items():
            self.assertIn('num_tweets', data)
            self.assertIn('total_likes', data)
            self.assertIn('total_retweets', data)
            self.assertIn('total_replies', data)
            self.assertIn('avg_likes', data)
            self.assertIn('avg_retweets', data)
            self.assertIn('avg_replies', data)
            self.assertIn('top_themes', data)
            
            self.assertIsInstance(data['num_tweets'], int)
            self.assertGreater(data['num_tweets'], 0)
    
    def test_get_top_hashtags(self):
        """Test top hashtags extraction."""
        top_hashtags = self.scraper.get_top_hashtags(self.sample_tweets, top_n=5)
        
        self.assertIsInstance(top_hashtags, list)
        self.assertGreater(len(top_hashtags), 0)
        
        # Verify structure
        for hashtag, count in top_hashtags:
            self.assertIsInstance(hashtag, str)
            self.assertIsInstance(count, int)
            self.assertGreater(count, 0)
        
        # Verify expected hashtags
        hashtag_names = [h for h, c in top_hashtags]
        self.assertIn("Health", hashtag_names)
        self.assertIn("Environment", hashtag_names)
    
    def test_get_handle_statistics(self):
        """Test handle statistics calculation."""
        stats = self.scraper.get_handle_statistics(self.sample_tweets)
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(len(stats), 3)  # 3 unique handles
        
        # Verify structure for each handle
        for handle, handle_stats in stats.items():
            self.assertIn('tweet_count', handle_stats)
            self.assertIn('total_likes', handle_stats)
            self.assertIn('total_retweets', handle_stats)
            self.assertIn('total_replies', handle_stats)
            self.assertIn('avg_likes', handle_stats)
            self.assertIn('avg_retweets', handle_stats)
            self.assertIn('avg_replies', handle_stats)
            self.assertIn('top_themes', handle_stats)
            
            self.assertGreater(handle_stats['tweet_count'], 0)
    
    def test_export_to_csv(self):
        """Test CSV export functionality."""
        filename = 'test_tweets.csv'
        self.scraper.export_to_csv(filename, self.sample_tweets)
        
        # Verify file exists
        self.assertTrue(os.path.exists(filename))
        
        # Verify content
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            self.assertEqual(len(rows), len(self.sample_tweets))
            
            # Verify headers
            self.assertIn('tweet_id', reader.fieldnames)
            self.assertIn('handle', reader.fieldnames)
            self.assertIn('text', reader.fieldnames)
            self.assertIn('likes', reader.fieldnames)
            self.assertIn('retweets', reader.fieldnames)
    
    def test_export_to_json(self):
        """Test JSON export functionality."""
        filename = 'test_tweets.json'
        self.scraper.export_to_json(filename, self.sample_tweets, 
                                    include_analysis=True)
        
        # Verify file exists
        self.assertTrue(os.path.exists(filename))
        
        # Verify content
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            
            self.assertIn('tweets', data)
            self.assertIn('metadata', data)
            self.assertIn('analysis', data)
            
            self.assertEqual(len(data['tweets']), len(self.sample_tweets))
            self.assertEqual(data['metadata']['total_tweets'], len(self.sample_tweets))
            
            # Verify analysis sections
            self.assertIn('themes', data['analysis'])
            self.assertIn('engagement_metrics', data['analysis'])
            self.assertIn('top_hashtags', data['analysis'])
            self.assertIn('handle_statistics', data['analysis'])
    
    def test_export_to_json_without_analysis(self):
        """Test JSON export without analysis."""
        filename = 'test_tweets.json'
        self.scraper.export_to_json(filename, self.sample_tweets, 
                                    include_analysis=False)
        
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            
            self.assertIn('tweets', data)
            self.assertIn('metadata', data)
            self.assertNotIn('analysis', data)
    
    def test_get_summary_report(self):
        """Test summary report generation."""
        report = self.scraper.get_summary_report(self.sample_tweets)
        
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)
        
        # Verify report contains expected sections
        self.assertIn("COMMUNICATION ANALYSIS", report)
        self.assertIn("COMMUNICATION THEMES", report)
        self.assertIn("ENGAGEMENT METRICS", report)
        self.assertIn("TOP HASHTAGS", report)
        self.assertIn("TOP PERFORMING HANDLES", report)
        
        # Verify report contains data
        self.assertIn("Total Tweets Analyzed", report)
        self.assertIn("Unique Handles", report)
    
    def test_get_summary_report_empty(self):
        """Test summary report with empty tweets."""
        report = self.scraper.get_summary_report([])
        
        self.assertIsInstance(report, str)
        self.assertIn("No tweets available", report)
    
    def test_get_theme_for_handle(self):
        """Test theme determination based on handle."""
        # Health-related handles
        self.assertEqual(self.scraper._get_theme_for_handle("@WHO"), "health")
        self.assertEqual(self.scraper._get_theme_for_handle("@MoHFW_INDIA"), "health")
        
        # Environment-related handles
        self.assertEqual(self.scraper._get_theme_for_handle("@WWF"), "environment")
        self.assertEqual(self.scraper._get_theme_for_handle("@Greenpeace"), "environment")
        
        # Disaster-related handles
        self.assertEqual(self.scraper._get_theme_for_handle("@ndmaindia"), "disaster")
        self.assertEqual(self.scraper._get_theme_for_handle("@fema"), "disaster")
        
        # Development-related handles
        self.assertEqual(self.scraper._get_theme_for_handle("@NITIAayog"), "development")
        self.assertEqual(self.scraper._get_theme_for_handle("@PMOIndia"), "development")
    
    def test_temporal_dynamics_weekly(self):
        """Test temporal dynamics with weekly interval."""
        temporal = self.scraper.analyze_temporal_dynamics(self.sample_tweets,
                                                         interval='weekly')
        
        self.assertIsInstance(temporal, dict)
        
        # Verify weekly format (YYYY-Wxx)
        for key in temporal.keys():
            self.assertRegex(key, r'\d{4}-W\d{2}')
    
    def test_temporal_dynamics_monthly(self):
        """Test temporal dynamics with monthly interval."""
        temporal = self.scraper.analyze_temporal_dynamics(self.sample_tweets,
                                                         interval='monthly')
        
        self.assertIsInstance(temporal, dict)
        
        # Verify monthly format (YYYY-MM)
        for key in temporal.keys():
            self.assertRegex(key, r'\d{4}-\d{2}')
    
    def test_integration_full_workflow(self):
        """Test complete workflow integration."""
        # Scrape tweets
        tweets = self.scraper.scrape_tweets(handles=["@UNICEF", "@WHO"], 
                                           max_tweets_per_handle=5,
                                           days_back=7)
        
        self.assertGreater(len(tweets), 0)
        
        # Analyze themes
        themes = self.scraper.analyze_themes(tweets)
        self.assertIsInstance(themes, dict)
        
        # Get engagement metrics
        metrics = self.scraper.get_engagement_metrics(tweets)
        self.assertIsInstance(metrics, EngagementMetrics)
        
        # Temporal analysis
        temporal = self.scraper.analyze_temporal_dynamics(tweets)
        self.assertIsInstance(temporal, dict)
        
        # Get top hashtags
        hashtags = self.scraper.get_top_hashtags(tweets)
        self.assertIsInstance(hashtags, list)
        
        # Get handle statistics
        handle_stats = self.scraper.get_handle_statistics(tweets)
        self.assertIsInstance(handle_stats, dict)
        
        # Generate report
        report = self.scraper.get_summary_report(tweets)
        self.assertIsInstance(report, str)
        
        # Export data
        self.scraper.export_to_csv('test_tweets.csv', tweets)
        self.assertTrue(os.path.exists('test_tweets.csv'))
        
        self.scraper.export_to_json('test_tweets.json', tweets, include_analysis=True)
        self.assertTrue(os.path.exists('test_tweets.json'))


class TestTweetDataClass(unittest.TestCase):
    """Test cases for Tweet data class."""
    
    def test_tweet_creation(self):
        """Test Tweet object creation."""
        tweet = Tweet(
            tweet_id="123",
            handle="@TestHandle",
            text="Test tweet #test",
            created_at=datetime.now().isoformat(),
            likes=100,
            retweets=20,
            replies=5,
            hashtags=["test"],
            mentions=["user"],
            url="https://twitter.com/test/status/123"
        )
        
        self.assertEqual(tweet.tweet_id, "123")
        self.assertEqual(tweet.handle, "@TestHandle")
        self.assertEqual(tweet.likes, 100)
        self.assertEqual(tweet.retweets, 20)
        self.assertEqual(tweet.replies, 5)
        self.assertEqual(len(tweet.hashtags), 1)
        self.assertEqual(len(tweet.mentions), 1)


class TestEngagementMetricsDataClass(unittest.TestCase):
    """Test cases for EngagementMetrics data class."""
    
    def test_engagement_metrics_creation(self):
        """Test EngagementMetrics object creation."""
        metrics = EngagementMetrics(
            total_likes=1000,
            total_retweets=200,
            total_replies=50,
            avg_likes=100.0,
            avg_retweets=20.0,
            avg_replies=5.0,
            engagement_rate=125.0
        )
        
        self.assertEqual(metrics.total_likes, 1000)
        self.assertEqual(metrics.total_retweets, 200)
        self.assertEqual(metrics.total_replies, 50)
        self.assertEqual(metrics.avg_likes, 100.0)
        self.assertEqual(metrics.avg_retweets, 20.0)
        self.assertEqual(metrics.avg_replies, 5.0)
        self.assertEqual(metrics.engagement_rate, 125.0)


if __name__ == '__main__':
    unittest.main()
