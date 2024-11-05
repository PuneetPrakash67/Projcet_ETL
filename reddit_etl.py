import os
import requests
import pandas as pd
import boto3
from io import StringIO
from datetime import datetime
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns

def run_reddit_etl():
    # Hardcoded Reddit API credentials
    client_id = "######"
    client_secret = "#######"
    user_agent = "#########"

    # Authenticate with Reddit API
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    headers = {"User-Agent": user_agent}
    data = {"grant_type": "password", "username": "#yourUsername", "password": "#######"}

    # Get the access token
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, headers=headers, data=data)
    if response.status_code != 200:
        print("Failed to fetch access token.")
        return
    
    token = response.json()["access_token"]
    headers["Authorization"] = f"bearer {token}"

    # Fetch posts from a subreddit
    subreddit = "google"  # Change to your preferred subreddit
    limit = 100  # Maximum limit per request
    total_posts = 100  # Total posts to fetch
    after = None  # This will be used for pagination

    post_list = []
    fetched_posts = 0

    print(f"Fetching {total_posts} posts from r/{subreddit}...")

    while fetched_posts < total_posts:
        url = f"https://oauth.reddit.com/r/{subreddit}/new?limit={limit}"
        if after:
            url += f"&after={after}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch posts: {response.status_code} {response.text}")
            return

        data = response.json()["data"]
        posts = data["children"]
        after = data.get("after")

        for post in posts:
            refined_post = {
                "title": post["data"]["title"],
                "author": post["data"]["author"],
                "score": post["data"]["score"],
                "created_utc": datetime.fromtimestamp(post["data"]["created_utc"]),
                "url": post["data"]["url"]
            }
            post_list.append(refined_post)

        fetched_posts += len(posts)
        print(f"Fetched {fetched_posts} posts so far...")

        if not after:
            break

    # Convert to DataFrame
    df = pd.DataFrame(post_list)
    print(f"DataFrame shape: {df.shape}")

    # Perform sentiment analysis
    sentiment_pipeline = pipeline("sentiment-analysis")
    df['sentiment'] = df['title'].apply(lambda x: sentiment_pipeline(x)[0]['label'])

    # Visualization of sentiment results
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(
        data=df,
        x='sentiment',
        order=df['sentiment'].value_counts().index,
        palette="coolwarm",  # Improved color scheme
        saturation=0.8
    )
    
    # Adding data labels on each bar for better readability
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + 0.3, p.get_height() + 1), ha='center')
    
    plt.title('Sentiment Analysis of Reddit Posts', fontsize=16)
    plt.xlabel('Sentiment', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a file
    plot_file_path = '/tmp/sentiment_analysis_plot.png'
    plt.savefig(plot_file_path)
    plt.close()

    # Save DataFrame to S3
    try:
        # Create a buffer for the DataFrame
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Upload DataFrame CSV to S3
        s3 = boto3.client('s3')
        s3.put_object(Bucket='#YOUR BUCKET NAME#', Key='refined_reddit_posts_with_sentiment.csv', Body=csv_buffer.getvalue())

        # Upload the plot to S3
        with open(plot_file_path, 'rb') as plot_file:
            s3.put_object(Bucket='#YOUR BUCKET NAME#', Key='sentiment_analysis_plot.png', Body=plot_file)

        print(f"ETL process completed. Posts and visualization saved to S3.")
    except Exception as e:
        print(f"Error uploading to S3: {e}")
