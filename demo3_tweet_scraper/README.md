# Tweet Scraper for Nonprofit Communication Analysis

A comprehensive tool for analyzing communication themes and engagement patterns from verified nonprofit organizations and public agencies on Twitter/X.

![Tweet Scraper Dashboard](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Overview

This tool scrapes and analyzes tweets from 40+ verified nonprofit and public agency handles to:

- **Extract Communication Themes**: Identify dominant themes (health, environment, disaster relief, etc.)
- **Track Engagement**: Analyze likes, retweets, and replies as engagement proxies
- **Examine Temporal Dynamics**: Study how communication patterns and engagement change over time
- **Compare Organizations**: Benchmark performance across different handles and sectors

## ✨ Features

### 🎯 Core Functionality

- **Curated Handle List**: 40+ verified nonprofit and public agency handles including:
  - International: UNICEF, WHO, WWF, UN agencies
  - Indian Government: NITI Aayog, Ministries, State agencies
  - Health Organizations: WHO, CDC, Red Cross, Gates Foundation
  - Environmental: WWF, Greenpeace, Conservation organizations
  - Disaster Relief: FEMA, NDMA, relief agencies

- **Theme Classification**: Automatic categorization into 8 major themes:
  - Health & Medicine
  - Education & Learning
  - Environment & Climate
  - Disaster & Emergency
  - Development & Policy
  - Social Welfare
  - Humanitarian Aid
  - Technology & Innovation

- **Engagement Metrics**:
  - Total and average likes/retweets/replies
  - Engagement rate calculations
  - Handle-wise performance comparison
  - Temporal engagement trends

- **Data Export**:
  - CSV format for spreadsheet analysis
  - JSON format with detailed analytics
  - Summary reports in text format

### 📊 Interactive Dashboard

- **Real-time Analysis**: Instant theme and engagement analysis
- **Visual Analytics**: Interactive charts using Plotly
- **Temporal Views**: Daily, weekly, and monthly aggregations
- **Customizable**: Filter by handle categories or select specific handles
- **Export Ready**: Download data and reports directly

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to the demo directory:**
   ```bash
   cd demo3_tweet_scraper
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Command Line Interface

Run the scraper directly from command line:

```bash
python tweet_scraper.py
```

This will:
- Scrape tweets from all verified handles (mock mode)
- Generate a comprehensive analysis report
- Export data to CSV and JSON files

#### Interactive Web Dashboard

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

Then open your browser to http://localhost:8501

#### Programmatic Usage

```python
from tweet_scraper import TweetScraper

# Initialize scraper
scraper = TweetScraper()

# Scrape tweets (mock mode for demonstration)
tweets = scraper.scrape_tweets(
    handles=["@UNICEF", "@WHO", "@WWF"],
    max_tweets_per_handle=50,
    days_back=30
)

# Analyze themes
themes = scraper.analyze_themes()
print(themes)

# Get engagement metrics
metrics = scraper.get_engagement_metrics()
print(f"Average engagement: {metrics.engagement_rate:.1f}")

# Analyze temporal dynamics
temporal = scraper.analyze_temporal_dynamics(interval='weekly')

# Export data
scraper.export_to_csv("tweets.csv")
scraper.export_to_json("tweets.json", include_analysis=True)

# Generate summary report
print(scraper.get_summary_report())
```

## 🔧 Configuration

### Mock Mode vs. Real API

By default, the scraper runs in **mock mode** for demonstration purposes, generating realistic sample data. This allows you to test and understand the tool without Twitter API credentials.

To use the real Twitter API:

```python
scraper = TweetScraper(
    bearer_token="YOUR_TWITTER_BEARER_TOKEN"
)
```

**Note**: Real API integration requires:
- Twitter Developer Account
- Approved API access
- Bearer token from Twitter Developer Portal

### Verified Handles

The tool includes 40+ curated handles, verified via:
- Public verification badges on Twitter/X
- Official websites linking to Twitter profiles
- Government and organization directories

To customize the handle list:

```python
# Use specific handles
custom_handles = ["@UNICEF", "@WHO", "@RedCross"]
tweets = scraper.scrape_tweets(handles=custom_handles)

# Or modify the default list
scraper.VERIFIED_HANDLES.extend(["@NewHandle1", "@NewHandle2"])
```

### Theme Classification

Customize theme keywords:

```python
scraper.COMMUNICATION_THEMES['custom_theme'] = [
    'keyword1', 'keyword2', 'keyword3'
]
```

## 📊 Analysis Features

### 1. Theme Analysis

Identifies dominant communication themes:

```python
themes = scraper.analyze_themes()
# Returns: {'health': 150, 'environment': 120, 'disaster': 80, ...}
```

### 2. Engagement Metrics

Comprehensive engagement statistics:

```python
metrics = scraper.get_engagement_metrics()
print(f"Total likes: {metrics.total_likes:,}")
print(f"Average engagement rate: {metrics.engagement_rate:.1f}")
```

### 3. Temporal Dynamics

Analyze patterns over time:

```python
# Daily aggregation
daily = scraper.analyze_temporal_dynamics(interval='daily')

# Weekly aggregation
weekly = scraper.analyze_temporal_dynamics(interval='weekly')

# Monthly aggregation
monthly = scraper.analyze_temporal_dynamics(interval='monthly')
```

### 4. Handle Statistics

Compare performance across handles:

```python
stats = scraper.get_handle_statistics()
for handle, data in stats.items():
    print(f"{handle}: {data['avg_likes']:.1f} avg likes")
```

### 5. Hashtag Analysis

Extract trending hashtags:

```python
top_hashtags = scraper.get_top_hashtags(top_n=20)
for hashtag, count in top_hashtags:
    print(f"#{hashtag}: {count} uses")
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python -m unittest test_tweet_scraper.py -v
```

Test coverage includes:
- Tweet scraping and data structures
- Theme classification algorithms
- Engagement metric calculations
- Temporal analysis functions
- Export functionality (CSV/JSON)
- Summary report generation
- Handle statistics
- Hashtag extraction
- Integration workflows

## 📈 Example Output

### Summary Report

```
======================================================================
NONPROFIT & PUBLIC AGENCY TWITTER COMMUNICATION ANALYSIS
======================================================================

Total Tweets Analyzed: 800
Unique Handles: 40
Analysis Date: 2024-01-15 10:30:00

----------------------------------------------------------------------
COMMUNICATION THEMES
----------------------------------------------------------------------
  HEALTH               245 tweets ( 30.6%)
  ENVIRONMENT          180 tweets ( 22.5%)
  DEVELOPMENT          150 tweets ( 18.8%)
  DISASTER              95 tweets ( 11.9%)
  SOCIAL_WELFARE        80 tweets ( 10.0%)
  EDUCATION             50 tweets (  6.2%)

----------------------------------------------------------------------
ENGAGEMENT METRICS
----------------------------------------------------------------------
  Total Likes:             245,600
  Total Retweets:           73,680
  Total Replies:            24,560
  Avg Likes/Tweet:             307.0
  Avg Retweets/Tweet:           92.1
  Avg Replies/Tweet:            30.7
  Engagement Rate:             429.8

----------------------------------------------------------------------
TOP HASHTAGS
----------------------------------------------------------------------
   1. #Health                   245 uses
   2. #ClimateAction            180 uses
   3. #DigitalIndia             150 uses
   4. #Vaccine                  120 uses
   5. #Conservation             115 uses
```

### Exported Data Structure

**CSV Format:**
```csv
tweet_id,handle,text,created_at,likes,retweets,replies,hashtags,mentions,url
1001,@UNICEF,"Vaccination...",2024-01-15T10:00:00,500,150,50,"Health,Vaccine",,https://...
```

**JSON Format:**
```json
{
  "tweets": [...],
  "metadata": {
    "total_tweets": 800,
    "export_date": "2024-01-15T10:30:00",
    "handles_count": 40
  },
  "analysis": {
    "themes": {...},
    "engagement_metrics": {...},
    "top_hashtags": [...],
    "handle_statistics": {...}
  }
}
```

## 🎓 Research Applications

This tool is designed for academic research on:

### Social Media Communication
- Organizational communication strategies
- Message framing and theme selection
- Crisis communication patterns
- Public engagement tactics

### Temporal Analysis
- Time-based trends in communication
- Seasonal patterns in themes
- Event-driven communication shifts
- Engagement fluctuations over time

### Comparative Studies
- Cross-organizational comparisons
- International vs. local agencies
- Sector-specific communication patterns
- Best practices in social media engagement

### Data Science & NLP
- Natural language processing applications
- Sentiment analysis (extensible)
- Topic modeling validation
- Social network analysis

## 🛠️ Technical Details

### Architecture

- **Core Module**: `tweet_scraper.py` - Main scraping and analysis logic
- **Web Interface**: `app.py` - Streamlit dashboard
- **Tests**: `test_tweet_scraper.py` - Comprehensive test suite
- **Data Classes**: Tweet and EngagementMetrics dataclasses for type safety

### Dependencies

- **tweepy**: Twitter API integration (for real mode)
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **streamlit**: Web dashboard framework
- **requests**: HTTP client for API calls

### Performance

- **Mock Mode**: Instant analysis of generated data
- **Real API**: Rate-limited by Twitter API (450 requests/15 min window)
- **Data Processing**: Handles 1000+ tweets efficiently
- **Export**: Fast CSV/JSON generation

## 📝 Data Privacy & Ethics

### Ethical Considerations

- ✅ Only scrapes **public** tweets from verified accounts
- ✅ Respects Twitter's Terms of Service and API limits
- ✅ No personal data collection from regular users
- ✅ Focuses on organizational communication only
- ✅ Mock mode available to avoid API usage for testing

### Data Usage

- Data collected is for research and analysis purposes
- No redistribution of raw tweet data without proper attribution
- Aggregated statistics and insights are shareable
- Follow institutional IRB guidelines if publishing research

## 🤝 Contributing

Suggestions for extensions:
- Sentiment analysis integration
- Multi-language support
- Advanced NLP features (topic modeling, entity recognition)
- Real-time streaming analysis
- Network analysis of mentions and interactions
- Automated report scheduling

## 📄 License

Part of the Academic_Demos collection - educational and demonstration purposes.

## 🔗 Related Demos

- **LectureKit**: AI-powered lecture recording and management
- **Grading Assistant**: Automated assignment feedback system

## 📧 Support

For questions or issues:
1. Check the test suite for usage examples
2. Review the inline documentation
3. Examine mock data generation for expected formats

## 🙏 Acknowledgments

This tool analyzes public communication from:
- International humanitarian organizations
- Indian government agencies and ministries
- Health and environmental NGOs
- Disaster relief organizations

Handle verification based on official websites and Twitter verification badges.
