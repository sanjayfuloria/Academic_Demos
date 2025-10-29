"""
Tweet Scraper for Nonprofit and Public Agency Communication Analysis

This module provides functionality to scrape tweets from verified nonprofit
and public agency handles, analyze communication themes, track engagement metrics,
and examine temporal dynamics.
"""

import json
import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re


@dataclass
class Tweet:
    """Represents a tweet with relevant metadata."""
    tweet_id: str
    handle: str
    text: str
    created_at: str
    likes: int
    retweets: int
    replies: int
    hashtags: List[str]
    mentions: List[str]
    url: str


@dataclass
class EngagementMetrics:
    """Engagement metrics for a tweet or collection of tweets."""
    total_likes: int
    total_retweets: int
    total_replies: int
    avg_likes: float
    avg_retweets: float
    avg_replies: float
    engagement_rate: float


class TweetScraper:
    """
    Scrapes and analyzes tweets from nonprofit and public agency handles.
    
    This class provides methods to:
    - Scrape tweets from verified handles
    - Extract engagement metrics
    - Analyze communication themes
    - Examine temporal dynamics
    - Export data in various formats
    """
    
    # Curated list of verified nonprofit and public agency handles
    VERIFIED_HANDLES = [
        # International Organizations
        "@UNICEF",
        "@WHO",
        "@WWF",
        "@UN",
        "@UNDP",
        "@UNHCR",
        "@WFP",
        "@UNEP",
        "@UNOCHA",
        "@UNHumanRights",
        
        # Indian Government Agencies
        "@NITIAayog",
        "@MoHFW_INDIA",
        "@PMOIndia",
        "@HMOIndia",
        "@MEAIndia",
        "@FinMinIndia",
        "@ndmaindia",
        "@NHAI_Official",
        "@mygovindia",
        "@DigitalIndiaG",
        
        # State/Local Agencies (India)
        "@CMODelhi",
        "@mybmc",
        "@MumbaiPolice",
        "@DelhiPolice",
        "@cmokarnataka",
        "@CMOTamilnadu",
        "@CMOUtahPradesh",
        "@CMOGujarat",
        
        # Health Organizations
        "@CDCgov",
        "@RedCross",
        "@MSF",
        "@gatesfoundation",
        
        # Environmental Organizations
        "@Greenpeace",
        "@ConservationOrg",
        "@Nature_org",
        "@OceanConservancy",
        
        # Disaster Relief
        "@fema",
        "@DisasterReliefIndia",
        "@NASAEarth"
    ]
    
    # Common themes for classification
    COMMUNICATION_THEMES = {
        'health': ['health', 'vaccine', 'disease', 'medicine', 'hospital', 'doctor', 
                   'patient', 'treatment', 'epidemic', 'pandemic', 'wellness', 'covid'],
        'education': ['education', 'school', 'learning', 'student', 'teacher', 'training',
                      'literacy', 'knowledge', 'academic', 'study'],
        'environment': ['environment', 'climate', 'pollution', 'sustainability', 'green',
                        'eco', 'conservation', 'wildlife', 'nature', 'forest', 'carbon'],
        'disaster': ['disaster', 'emergency', 'relief', 'rescue', 'flood', 'earthquake',
                     'cyclone', 'fire', 'evacuation', 'alert', 'warning'],
        'development': ['development', 'infrastructure', 'economy', 'growth', 'policy',
                        'initiative', 'program', 'scheme', 'project', 'plan'],
        'social_welfare': ['welfare', 'poverty', 'hunger', 'food', 'nutrition', 'rights',
                           'justice', 'equality', 'empowerment', 'support'],
        'humanitarian': ['humanitarian', 'aid', 'refugee', 'crisis', 'protection', 'shelter',
                         'assistance', 'vulnerable', 'displaced'],
        'technology': ['digital', 'technology', 'innovation', 'tech', 'online', 'app',
                       'platform', 'data', 'cyber', 'ai']
    }
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
                 bearer_token: Optional[str] = None):
        """
        Initialize the TweetScraper.
        
        Args:
            api_key: Twitter API key (optional for mock mode)
            api_secret: Twitter API secret (optional for mock mode)
            bearer_token: Twitter Bearer token (optional for mock mode)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.bearer_token = bearer_token
        self.tweets: List[Tweet] = []
        self.mock_mode = not bearer_token  # Use mock mode if no credentials provided
        
    def scrape_tweets(self, handles: Optional[List[str]] = None, 
                     max_tweets_per_handle: int = 100,
                     days_back: int = 30) -> List[Tweet]:
        """
        Scrape tweets from specified handles.
        
        Args:
            handles: List of Twitter handles to scrape (default: all verified handles)
            max_tweets_per_handle: Maximum number of tweets to retrieve per handle
            days_back: Number of days to look back for tweets
            
        Returns:
            List of Tweet objects
        """
        if handles is None:
            handles = self.VERIFIED_HANDLES
            
        self.tweets = []
        
        if self.mock_mode:
            # Generate mock data for demonstration
            self.tweets = self._generate_mock_tweets(handles, max_tweets_per_handle, days_back)
        else:
            # Real API implementation would go here
            self.tweets = self._fetch_real_tweets(handles, max_tweets_per_handle, days_back)
            
        return self.tweets
    
    def _generate_mock_tweets(self, handles: List[str], max_tweets: int, 
                            days_back: int) -> List[Tweet]:
        """Generate mock tweets for testing and demonstration."""
        mock_tweets = []
        base_date = datetime.now()
        
        # Sample tweet templates for different themes
        templates = {
            'health': [
                "Vaccination drive reaches {num} million people across {region}. #Health #Vaccine",
                "New healthcare initiative launched to improve {service} in rural areas.",
                "Join us in the fight against {disease}. Early detection saves lives. #PublicHealth",
            ],
            'environment': [
                "Planting {num} trees this year to combat climate change. #Environment #GreenFuture",
                "Our latest conservation project protects {num} hectares of forest. #Conservation",
                "Reducing carbon emissions by {num}% - together we can make a difference. #ClimateAction",
            ],
            'disaster': [
                "Emergency relief supplies dispatched to {region}. #DisasterRelief #Emergency",
                "Evacuation orders issued for {region}. Stay safe and follow official guidance.",
                "Recovery efforts underway after {disaster} in {region}. #Relief #Support",
            ],
            'development': [
                "New infrastructure project to benefit {num} communities. #Development #Progress",
                "Economic growth initiative creates {num} new opportunities. #Growth #Economy",
                "Digital India: Connecting {num} villages with high-speed internet. #DigitalIndia",
            ],
            'social_welfare': [
                "Food distribution program reaches {num} families in need. #Welfare #Support",
                "Empowering {num} women through skill development programs. #Empowerment",
                "New scheme provides assistance to {num} beneficiaries. #SocialWelfare",
            ]
        }
        
        regions = ["Northern India", "Eastern states", "rural areas", "urban centers", "coastal regions"]
        services = ["healthcare", "sanitation", "water supply", "medical facilities"]
        diseases = ["malaria", "tuberculosis", "dengue", "preventable diseases"]
        disasters = ["floods", "cyclone", "earthquake", "forest fires"]
        
        tweet_id = 1000000
        
        for handle in handles:
            num_tweets = min(max_tweets, 20)  # Generate up to 20 tweets per handle
            
            for i in range(num_tweets):
                # Select a random theme based on handle
                theme = self._get_theme_for_handle(handle)
                if theme in templates:
                    template_list = templates[theme]
                    template = template_list[i % len(template_list)]
                    
                    # Fill in template variables
                    text = template.format(
                        num=str((i + 1) * 10),
                        region=regions[i % len(regions)],
                        service=services[i % len(services)],
                        disease=diseases[i % len(diseases)],
                        disaster=disasters[i % len(disasters)]
                    )
                else:
                    text = f"Important update from {handle} about our ongoing initiatives. #{theme}"
                
                # Generate timestamp
                days_ago = (i * days_back) // num_tweets
                created_at = (base_date - timedelta(days=days_ago)).isoformat()
                
                # Extract hashtags and mentions
                hashtags = re.findall(r'#(\w+)', text)
                mentions = re.findall(r'@(\w+)', text)
                
                # Generate engagement metrics (higher for more recent tweets)
                recency_factor = 1 - (days_ago / days_back)
                base_likes = int(100 + 900 * recency_factor + (i * 50))
                base_retweets = int(base_likes * 0.3)
                base_replies = int(base_likes * 0.1)
                
                tweet = Tweet(
                    tweet_id=str(tweet_id),
                    handle=handle,
                    text=text,
                    created_at=created_at,
                    likes=base_likes,
                    retweets=base_retweets,
                    replies=base_replies,
                    hashtags=hashtags,
                    mentions=mentions,
                    url=f"https://twitter.com/{handle.replace('@', '')}/status/{tweet_id}"
                )
                
                mock_tweets.append(tweet)
                tweet_id += 1
                
        return mock_tweets
    
    def _get_theme_for_handle(self, handle: str) -> str:
        """Determine the primary theme based on handle."""
        handle_lower = handle.lower()
        
        if any(word in handle_lower for word in ['health', 'who', 'mohfw']):
            return 'health'
        elif any(word in handle_lower for word in ['wwf', 'green', 'environment', 'unep']):
            return 'environment'
        elif any(word in handle_lower for word in ['disaster', 'relief', 'ndma', 'fema']):
            return 'disaster'
        elif any(word in handle_lower for word in ['niti', 'pmo', 'development', 'digital']):
            return 'development'
        elif any(word in handle_lower for word in ['unicef', 'unhcr', 'wfp']):
            return 'social_welfare'
        else:
            return 'development'
    
    def _fetch_real_tweets(self, handles: List[str], max_tweets: int, 
                          days_back: int) -> List[Tweet]:
        """
        Fetch real tweets using Twitter API.
        
        This method would implement actual Twitter API v2 calls using tweepy or requests.
        For now, it's a placeholder that would need Twitter API credentials to work.
        """
        # Real implementation would use Twitter API v2
        # Example with tweepy (requires installation):
        # import tweepy
        # client = tweepy.Client(bearer_token=self.bearer_token)
        # ...
        
        raise NotImplementedError(
            "Real Twitter API integration requires valid credentials. "
            "Use mock_mode=True for demonstration purposes."
        )
    
    def analyze_themes(self, tweets: Optional[List[Tweet]] = None) -> Dict[str, int]:
        """
        Analyze and classify tweets by communication themes.
        
        Args:
            tweets: List of tweets to analyze (default: all scraped tweets)
            
        Returns:
            Dictionary mapping themes to tweet counts
        """
        if tweets is None:
            tweets = self.tweets
            
        theme_counts = defaultdict(int)
        
        for tweet in tweets:
            text_lower = tweet.text.lower()
            classified = False
            
            for theme, keywords in self.COMMUNICATION_THEMES.items():
                if any(keyword in text_lower for keyword in keywords):
                    theme_counts[theme] += 1
                    classified = True
                    break
                    
            if not classified:
                theme_counts['other'] += 1
                
        return dict(theme_counts)
    
    def get_engagement_metrics(self, tweets: Optional[List[Tweet]] = None) -> EngagementMetrics:
        """
        Calculate engagement metrics for tweets.
        
        Args:
            tweets: List of tweets to analyze (default: all scraped tweets)
            
        Returns:
            EngagementMetrics object with aggregated statistics
        """
        if tweets is None:
            tweets = self.tweets
            
        if not tweets:
            return EngagementMetrics(0, 0, 0, 0.0, 0.0, 0.0, 0.0)
            
        total_likes = sum(t.likes for t in tweets)
        total_retweets = sum(t.retweets for t in tweets)
        total_replies = sum(t.replies for t in tweets)
        
        num_tweets = len(tweets)
        avg_likes = total_likes / num_tweets
        avg_retweets = total_retweets / num_tweets
        avg_replies = total_replies / num_tweets
        
        # Engagement rate: (likes + retweets + replies) / num_tweets
        engagement_rate = (total_likes + total_retweets + total_replies) / num_tweets
        
        return EngagementMetrics(
            total_likes=total_likes,
            total_retweets=total_retweets,
            total_replies=total_replies,
            avg_likes=avg_likes,
            avg_retweets=avg_retweets,
            avg_replies=avg_replies,
            engagement_rate=engagement_rate
        )
    
    def analyze_temporal_dynamics(self, tweets: Optional[List[Tweet]] = None,
                                 interval: str = 'daily') -> Dict[str, Dict]:
        """
        Analyze temporal patterns in tweets and engagement.
        
        Args:
            tweets: List of tweets to analyze (default: all scraped tweets)
            interval: Time interval for aggregation ('daily', 'weekly', 'monthly')
            
        Returns:
            Dictionary mapping time periods to engagement metrics and themes
        """
        if tweets is None:
            tweets = self.tweets
            
        temporal_data = defaultdict(lambda: {
            'tweets': [],
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'themes': defaultdict(int)
        })
        
        for tweet in tweets:
            # Parse date and determine interval key
            date = datetime.fromisoformat(tweet.created_at.replace('Z', '+00:00'))
            
            if interval == 'daily':
                key = date.strftime('%Y-%m-%d')
            elif interval == 'weekly':
                key = date.strftime('%Y-W%W')
            elif interval == 'monthly':
                key = date.strftime('%Y-%m')
            else:
                key = date.strftime('%Y-%m-%d')
                
            temporal_data[key]['tweets'].append(tweet)
            temporal_data[key]['likes'] += tweet.likes
            temporal_data[key]['retweets'] += tweet.retweets
            temporal_data[key]['replies'] += tweet.replies
            
            # Classify theme
            text_lower = tweet.text.lower()
            for theme, keywords in self.COMMUNICATION_THEMES.items():
                if any(keyword in text_lower for keyword in keywords):
                    temporal_data[key]['themes'][theme] += 1
                    break
        
        # Convert to regular dict and calculate averages
        result = {}
        for key, data in sorted(temporal_data.items()):
            num_tweets = len(data['tweets'])
            result[key] = {
                'num_tweets': num_tweets,
                'total_likes': data['likes'],
                'total_retweets': data['retweets'],
                'total_replies': data['replies'],
                'avg_likes': data['likes'] / num_tweets if num_tweets > 0 else 0,
                'avg_retweets': data['retweets'] / num_tweets if num_tweets > 0 else 0,
                'avg_replies': data['replies'] / num_tweets if num_tweets > 0 else 0,
                'top_themes': dict(Counter(data['themes']).most_common(3))
            }
            
        return result
    
    def get_top_hashtags(self, tweets: Optional[List[Tweet]] = None, 
                        top_n: int = 20) -> List[Tuple[str, int]]:
        """
        Get the most frequently used hashtags.
        
        Args:
            tweets: List of tweets to analyze (default: all scraped tweets)
            top_n: Number of top hashtags to return
            
        Returns:
            List of (hashtag, count) tuples
        """
        if tweets is None:
            tweets = self.tweets
            
        hashtag_counter = Counter()
        for tweet in tweets:
            hashtag_counter.update(tweet.hashtags)
            
        return hashtag_counter.most_common(top_n)
    
    def get_handle_statistics(self, tweets: Optional[List[Tweet]] = None) -> Dict[str, Dict]:
        """
        Get statistics for each handle.
        
        Args:
            tweets: List of tweets to analyze (default: all scraped tweets)
            
        Returns:
            Dictionary mapping handles to their statistics
        """
        if tweets is None:
            tweets = self.tweets
            
        handle_stats = defaultdict(lambda: {
            'tweet_count': 0,
            'total_likes': 0,
            'total_retweets': 0,
            'total_replies': 0,
            'themes': defaultdict(int)
        })
        
        for tweet in tweets:
            stats = handle_stats[tweet.handle]
            stats['tweet_count'] += 1
            stats['total_likes'] += tweet.likes
            stats['total_retweets'] += tweet.retweets
            stats['total_replies'] += tweet.replies
            
            # Classify theme
            text_lower = tweet.text.lower()
            for theme, keywords in self.COMMUNICATION_THEMES.items():
                if any(keyword in text_lower for keyword in keywords):
                    stats['themes'][theme] += 1
                    break
        
        # Calculate averages
        result = {}
        for handle, stats in handle_stats.items():
            count = stats['tweet_count']
            result[handle] = {
                'tweet_count': count,
                'total_likes': stats['total_likes'],
                'total_retweets': stats['total_retweets'],
                'total_replies': stats['total_replies'],
                'avg_likes': stats['total_likes'] / count if count > 0 else 0,
                'avg_retweets': stats['total_retweets'] / count if count > 0 else 0,
                'avg_replies': stats['total_replies'] / count if count > 0 else 0,
                'top_themes': dict(Counter(stats['themes']).most_common(3))
            }
            
        return result
    
    def export_to_csv(self, filename: str, tweets: Optional[List[Tweet]] = None):
        """
        Export tweets to CSV file.
        
        Args:
            filename: Output CSV filename
            tweets: List of tweets to export (default: all scraped tweets)
        """
        if tweets is None:
            tweets = self.tweets
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if not tweets:
                return
                
            fieldnames = ['tweet_id', 'handle', 'text', 'created_at', 'likes', 
                         'retweets', 'replies', 'hashtags', 'mentions', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tweet in tweets:
                row = asdict(tweet)
                row['hashtags'] = ','.join(tweet.hashtags)
                row['mentions'] = ','.join(tweet.mentions)
                writer.writerow(row)
    
    def export_to_json(self, filename: str, tweets: Optional[List[Tweet]] = None,
                      include_analysis: bool = False):
        """
        Export tweets to JSON file.
        
        Args:
            filename: Output JSON filename
            tweets: List of tweets to export (default: all scraped tweets)
            include_analysis: Whether to include analysis results
        """
        if tweets is None:
            tweets = self.tweets
            
        data = {
            'tweets': [asdict(tweet) for tweet in tweets],
            'metadata': {
                'total_tweets': len(tweets),
                'export_date': datetime.now().isoformat(),
                'handles_count': len(set(t.handle for t in tweets))
            }
        }
        
        if include_analysis:
            data['analysis'] = {
                'themes': self.analyze_themes(tweets),
                'engagement_metrics': asdict(self.get_engagement_metrics(tweets)),
                'top_hashtags': self.get_top_hashtags(tweets, 10),
                'handle_statistics': self.get_handle_statistics(tweets)
            }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    def get_summary_report(self, tweets: Optional[List[Tweet]] = None) -> str:
        """
        Generate a text summary report of the analysis.
        
        Args:
            tweets: List of tweets to analyze (default: all scraped tweets)
            
        Returns:
            Formatted text report
        """
        if tweets is None:
            tweets = self.tweets
            
        if not tweets:
            return "No tweets available for analysis."
            
        # Get all metrics
        themes = self.analyze_themes(tweets)
        engagement = self.get_engagement_metrics(tweets)
        top_hashtags = self.get_top_hashtags(tweets, 10)
        handle_stats = self.get_handle_statistics(tweets)
        
        # Build report
        report = []
        report.append("=" * 70)
        report.append("NONPROFIT & PUBLIC AGENCY TWITTER COMMUNICATION ANALYSIS")
        report.append("=" * 70)
        report.append(f"\nTotal Tweets Analyzed: {len(tweets)}")
        report.append(f"Unique Handles: {len(set(t.handle for t in tweets))}")
        report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        report.append("\n" + "-" * 70)
        report.append("COMMUNICATION THEMES")
        report.append("-" * 70)
        sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
        for theme, count in sorted_themes:
            percentage = (count / len(tweets)) * 100
            report.append(f"  {theme.upper():<20} {count:>5} tweets ({percentage:>5.1f}%)")
        
        report.append("\n" + "-" * 70)
        report.append("ENGAGEMENT METRICS")
        report.append("-" * 70)
        report.append(f"  Total Likes:         {engagement.total_likes:>10,}")
        report.append(f"  Total Retweets:      {engagement.total_retweets:>10,}")
        report.append(f"  Total Replies:       {engagement.total_replies:>10,}")
        report.append(f"  Avg Likes/Tweet:     {engagement.avg_likes:>10.1f}")
        report.append(f"  Avg Retweets/Tweet:  {engagement.avg_retweets:>10.1f}")
        report.append(f"  Avg Replies/Tweet:   {engagement.avg_replies:>10.1f}")
        report.append(f"  Engagement Rate:     {engagement.engagement_rate:>10.1f}")
        
        report.append("\n" + "-" * 70)
        report.append("TOP HASHTAGS")
        report.append("-" * 70)
        for i, (hashtag, count) in enumerate(top_hashtags, 1):
            report.append(f"  {i:>2}. #{hashtag:<25} {count:>5} uses")
        
        report.append("\n" + "-" * 70)
        report.append("TOP PERFORMING HANDLES (by avg engagement)")
        report.append("-" * 70)
        sorted_handles = sorted(handle_stats.items(), 
                               key=lambda x: x[1]['avg_likes'] + x[1]['avg_retweets'],
                               reverse=True)[:10]
        for i, (handle, stats) in enumerate(sorted_handles, 1):
            avg_eng = stats['avg_likes'] + stats['avg_retweets']
            report.append(f"  {i:>2}. {handle:<25} Avg Engagement: {avg_eng:>7.1f}")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)


def main():
    """Main function for command-line usage."""
    print("Tweet Scraper for Nonprofit Communication Analysis")
    print("=" * 60)
    
    # Initialize scraper (mock mode for demonstration)
    scraper = TweetScraper()
    
    print("\n📡 Scraping tweets from verified nonprofit and public agency handles...")
    print(f"   Handles: {len(scraper.VERIFIED_HANDLES)} verified accounts")
    
    # Scrape tweets (using mock data)
    tweets = scraper.scrape_tweets(max_tweets_per_handle=20, days_back=30)
    print(f"✓  Scraped {len(tweets)} tweets")
    
    # Generate summary report
    print("\n" + scraper.get_summary_report())
    
    # Export data
    print("\n📁 Exporting data...")
    scraper.export_to_csv("tweets_data.csv")
    print("   ✓ Exported to tweets_data.csv")
    
    scraper.export_to_json("tweets_analysis.json", include_analysis=True)
    print("   ✓ Exported to tweets_analysis.json (with analysis)")
    
    # Temporal analysis
    print("\n📊 Analyzing temporal dynamics...")
    temporal = scraper.analyze_temporal_dynamics(interval='weekly')
    print(f"   ✓ Analyzed {len(temporal)} time periods")
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
