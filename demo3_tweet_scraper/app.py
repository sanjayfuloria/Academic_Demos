"""
Streamlit Web Interface for Tweet Scraper

Interactive dashboard for analyzing nonprofit and public agency communication on Twitter/X.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from tweet_scraper import TweetScraper


# Page configuration
st.set_page_config(
    page_title="Nonprofit Tweet Analyzer",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def load_tweets(handles, max_tweets, days_back):
    """Load and cache tweet data."""
    scraper = TweetScraper()
    tweets = scraper.scrape_tweets(handles=handles if handles else None,
                                   max_tweets_per_handle=max_tweets,
                                   days_back=days_back)
    return scraper, tweets


def create_theme_chart(themes):
    """Create a bar chart for communication themes."""
    df = pd.DataFrame(list(themes.items()), columns=['Theme', 'Count'])
    df = df.sort_values('Count', ascending=True)
    
    fig = px.bar(df, x='Count', y='Theme', orientation='h',
                 title='Communication Themes Distribution',
                 labels={'Count': 'Number of Tweets', 'Theme': 'Theme'},
                 color='Count',
                 color_continuous_scale='Blues')
    
    fig.update_layout(height=400, showlegend=False)
    return fig


def create_engagement_chart(handle_stats):
    """Create a scatter plot for handle engagement."""
    data = []
    for handle, stats in handle_stats.items():
        data.append({
            'Handle': handle,
            'Avg Likes': stats['avg_likes'],
            'Avg Retweets': stats['avg_retweets'],
            'Tweet Count': stats['tweet_count'],
            'Total Engagement': stats['avg_likes'] + stats['avg_retweets']
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('Total Engagement', ascending=False).head(15)
    
    fig = px.scatter(df, x='Avg Likes', y='Avg Retweets', 
                     size='Tweet Count', hover_name='Handle',
                     title='Handle Engagement Analysis (Top 15)',
                     labels={'Avg Likes': 'Average Likes', 
                            'Avg Retweets': 'Average Retweets'},
                     color='Total Engagement',
                     color_continuous_scale='Viridis',
                     size_max=30)
    
    fig.update_layout(height=500)
    return fig


def create_temporal_chart(temporal_data, metric='num_tweets'):
    """Create a line chart for temporal dynamics."""
    dates = []
    values = []
    
    for date_str, data in sorted(temporal_data.items()):
        dates.append(date_str)
        values.append(data[metric])
    
    df = pd.DataFrame({'Date': dates, 'Value': values})
    
    metric_labels = {
        'num_tweets': 'Number of Tweets',
        'total_likes': 'Total Likes',
        'total_retweets': 'Total Retweets',
        'avg_likes': 'Average Likes per Tweet'
    }
    
    fig = px.line(df, x='Date', y='Value',
                  title=f'Temporal Dynamics: {metric_labels.get(metric, metric)}',
                  labels={'Date': 'Date', 'Value': metric_labels.get(metric, metric)},
                  markers=True)
    
    fig.update_layout(height=400)
    return fig


def create_hashtag_cloud(top_hashtags):
    """Create a word cloud visualization for hashtags."""
    if not top_hashtags:
        return None
    
    hashtags = [f"#{h}" for h, c in top_hashtags]
    counts = [c for h, c in top_hashtags]
    
    df = pd.DataFrame({'Hashtag': hashtags, 'Count': counts})
    df = df.sort_values('Count', ascending=False).head(15)
    
    fig = px.bar(df, x='Count', y='Hashtag', orientation='h',
                 title='Top Hashtags',
                 labels={'Count': 'Usage Count', 'Hashtag': 'Hashtag'},
                 color='Count',
                 color_continuous_scale='Greens')
    
    fig.update_layout(height=500, showlegend=False)
    return fig


def main():
    """Main Streamlit application."""
    
    # Header
    st.title("📊 Nonprofit & Public Agency Tweet Analyzer")
    st.markdown("""
    Analyze communication themes and engagement patterns from verified nonprofit 
    organizations and public agencies on Twitter/X.
    """)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Initialize scraper to get handle list
    temp_scraper = TweetScraper()
    
    # Handle selection
    st.sidebar.subheader("Select Handles")
    handle_selection = st.sidebar.selectbox(
        "Choose handle set:",
        ["All Verified Handles", "International Orgs", "Indian Government", 
         "Health Orgs", "Environmental Orgs", "Custom Selection"]
    )
    
    selected_handles = None
    if handle_selection == "International Orgs":
        selected_handles = [h for h in temp_scraper.VERIFIED_HANDLES 
                           if any(x in h for x in ["@UN", "@WHO", "@UNICEF", "@WWF", "@WFP"])]
    elif handle_selection == "Indian Government":
        selected_handles = [h for h in temp_scraper.VERIFIED_HANDLES 
                           if any(x in h for x in ["@NITI", "@MoHFW", "@PMO", "@HMO", "@CMO"])]
    elif handle_selection == "Health Orgs":
        selected_handles = [h for h in temp_scraper.VERIFIED_HANDLES 
                           if any(x in h.lower() for x in ["health", "who", "cdc", "red"])]
    elif handle_selection == "Environmental Orgs":
        selected_handles = [h for h in temp_scraper.VERIFIED_HANDLES 
                           if any(x in h.lower() for x in ["wwf", "green", "conservation", "nature"])]
    elif handle_selection == "Custom Selection":
        selected_handles = st.sidebar.multiselect(
            "Select specific handles:",
            temp_scraper.VERIFIED_HANDLES,
            default=temp_scraper.VERIFIED_HANDLES[:5]
        )
    
    # Scraping parameters
    st.sidebar.subheader("Scraping Parameters")
    max_tweets = st.sidebar.slider("Tweets per handle:", 5, 50, 20)
    days_back = st.sidebar.slider("Days to look back:", 7, 90, 30)
    
    # Load data button
    if st.sidebar.button("🔍 Analyze Tweets", type="primary"):
        with st.spinner("Scraping and analyzing tweets..."):
            scraper, tweets = load_tweets(selected_handles, max_tweets, days_back)
            st.session_state.scraper = scraper
            st.session_state.tweets = tweets
    
    # Main content
    if 'tweets' not in st.session_state or not st.session_state.tweets:
        st.info("👈 Configure settings in the sidebar and click 'Analyze Tweets' to start.")
        
        # Show sample info
        st.subheader("📋 About This Tool")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Features:**
            - Extract tweets from 40+ verified handles
            - Analyze communication themes
            - Track engagement metrics (likes/retweets)
            - Examine temporal dynamics
            - Export data for further analysis
            """)
        
        with col2:
            st.markdown("""
            **Verified Handles Include:**
            - International: UNICEF, WHO, WWF, UN agencies
            - Indian Govt: NITI Aayog, Ministries, PMO
            - Health: WHO, CDC, Red Cross, Gates Foundation
            - Environment: WWF, Greenpeace, Conservation orgs
            - Disaster: FEMA, NDMA, relief agencies
            """)
        
        return
    
    scraper = st.session_state.scraper
    tweets = st.session_state.tweets
    
    # Overview metrics
    st.header("📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tweets", len(tweets))
    
    with col2:
        unique_handles = len(set(t.handle for t in tweets))
        st.metric("Unique Handles", unique_handles)
    
    engagement_metrics = scraper.get_engagement_metrics(tweets)
    
    with col3:
        st.metric("Total Engagement", 
                 f"{engagement_metrics.total_likes + engagement_metrics.total_retweets:,}")
    
    with col4:
        st.metric("Avg Engagement/Tweet",
                 f"{engagement_metrics.engagement_rate:.1f}")
    
    # Theme Analysis
    st.header("🎯 Communication Themes")
    
    themes = scraper.analyze_themes(tweets)
    fig_themes = create_theme_chart(themes)
    st.plotly_chart(fig_themes, use_container_width=True)
    
    # Theme details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Theme Distribution")
        theme_df = pd.DataFrame(list(themes.items()), columns=['Theme', 'Count'])
        theme_df['Percentage'] = (theme_df['Count'] / len(tweets) * 100).round(1)
        theme_df = theme_df.sort_values('Count', ascending=False)
        st.dataframe(theme_df, hide_index=True, use_container_width=True)
    
    with col2:
        st.subheader("Top Hashtags")
        top_hashtags = scraper.get_top_hashtags(tweets, top_n=10)
        hashtag_df = pd.DataFrame(top_hashtags, columns=['Hashtag', 'Count'])
        st.dataframe(hashtag_df, hide_index=True, use_container_width=True)
    
    # Engagement Analysis
    st.header("💬 Engagement Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Likes", f"{engagement_metrics.total_likes:,}")
        st.metric("Avg Likes/Tweet", f"{engagement_metrics.avg_likes:.1f}")
    
    with col2:
        st.metric("Total Retweets", f"{engagement_metrics.total_retweets:,}")
        st.metric("Avg Retweets/Tweet", f"{engagement_metrics.avg_retweets:.1f}")
    
    # Handle engagement scatter plot
    handle_stats = scraper.get_handle_statistics(tweets)
    fig_engagement = create_engagement_chart(handle_stats)
    st.plotly_chart(fig_engagement, use_container_width=True)
    
    # Temporal Dynamics
    st.header("📅 Temporal Dynamics")
    
    interval = st.selectbox("Time Interval:", ["daily", "weekly", "monthly"])
    temporal_data = scraper.analyze_temporal_dynamics(tweets, interval=interval)
    
    metric_choice = st.selectbox(
        "Select Metric:",
        ["num_tweets", "total_likes", "total_retweets", "avg_likes"],
        format_func=lambda x: {
            'num_tweets': 'Number of Tweets',
            'total_likes': 'Total Likes',
            'total_retweets': 'Total Retweets',
            'avg_likes': 'Average Likes per Tweet'
        }[x]
    )
    
    fig_temporal = create_temporal_chart(temporal_data, metric_choice)
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Top Performing Handles
    st.header("🏆 Top Performing Handles")
    
    handle_data = []
    for handle, stats in handle_stats.items():
        handle_data.append({
            'Handle': handle,
            'Tweets': stats['tweet_count'],
            'Total Likes': stats['total_likes'],
            'Total Retweets': stats['total_retweets'],
            'Avg Likes': round(stats['avg_likes'], 1),
            'Avg Retweets': round(stats['avg_retweets'], 1),
            'Top Theme': max(stats['top_themes'].items(), key=lambda x: x[1])[0] if stats['top_themes'] else 'N/A'
        })
    
    handle_df = pd.DataFrame(handle_data)
    handle_df = handle_df.sort_values('Total Likes', ascending=False).head(15)
    st.dataframe(handle_df, hide_index=True, use_container_width=True)
    
    # Hashtag Visualization
    st.header("#️⃣ Hashtag Analysis")
    top_hashtags = scraper.get_top_hashtags(tweets, top_n=20)
    fig_hashtags = create_hashtag_cloud(top_hashtags)
    st.plotly_chart(fig_hashtags, use_container_width=True)
    
    # Export Options
    st.header("💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate Summary Report"):
            report = scraper.get_summary_report(tweets)
            st.text_area("Summary Report", report, height=400)
    
    with col2:
        if st.button("📊 Export to CSV"):
            scraper.export_to_csv("tweets_data.csv", tweets)
            st.success("✅ Exported to tweets_data.csv")
            with open("tweets_data.csv", "r") as f:
                st.download_button("Download CSV", f, "tweets_data.csv", "text/csv")
    
    with col3:
        if st.button("📋 Export to JSON"):
            scraper.export_to_json("tweets_analysis.json", tweets, include_analysis=True)
            st.success("✅ Exported to tweets_analysis.json")
            with open("tweets_analysis.json", "r") as f:
                st.download_button("Download JSON", f, "tweets_analysis.json", "application/json")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Tweet Scraper for Nonprofit Communication Analysis | Academic Demo</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
