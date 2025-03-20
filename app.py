import requests
import torch
from bark import generate_audio, preload_models
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import streamlit as st
import os
import re
import soundfile as sf

def extract_news(company_name):
    """Extracts news articles from Google News RSS feed."""
    search_url = f"https://news.google.com/rss/search?q={company_name}"
    response = requests.get(search_url)

    if response.status_code != 200:
        st.error("Failed to fetch news. Please try again later.")
        return []

    soup = BeautifulSoup(response.content, "xml")  # Use XML parser for RSS feeds
    items = soup.find_all("item")  # Extracting news articles

    news_data = []
    for item in items[:10]:  # Get first 10 news articles
        title = item.find("title").text if item.find("title") else "No Title"
        description_tag = item.find("description")
        summary = description_tag.text if description_tag else "No Summary"
        
        # Remove unwanted HTML tags from summary
        summary = re.sub(r'<.*?>', '', summary)

        link = item.find("link").text if item.find("link") else item.find("guid").text if item.find("guid") else "#"

        news_data.append({"title": title, "summary": summary, "link": link})

    return news_data

def analyze_sentiment(news_data):
    """Performs sentiment analysis on the news summaries."""
    analyzer = SentimentIntensityAnalyzer()
    sentiment_results = []

    for news in news_data:
        score = analyzer.polarity_scores(news["summary"])
        if score['compound'] >= 0.05:
            sentiment = "Positive"
        elif score['compound'] <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        news["sentiment"] = sentiment
        sentiment_results.append(news)

    return sentiment_results

def generate_comparative_analysis(sentiment_results):
    """Generates sentiment summary across all news articles."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for result in sentiment_results:
        sentiment_counts[result["sentiment"]] += 1

    return sentiment_counts

device = "cuda" if torch.cuda.is_available() else "cpu"

def text_to_speech(text):
    """Convert text to Hindi speech using Bark (with weight loading fix)."""
    torch.serialization.add_safe_globals([torch.serialization.UntypedStorage])  # Allow globals
    preload_models()
    audio_array = generate_audio(text, history_prompt="hi_speaker")
    audio_path = "output.wav"
    sf.write(audio_path, audio_array, samplerate=24000)
    return audio_path


def main():
    st.title("📊 Company News Sentiment Analyzer")
    company_name = st.text_input("🔍 Enter Company Name")

    if st.button("Analyze"):
        news_data = extract_news(company_name)

        if not news_data:
            st.warning("No relevant news found. Try another company.")
            return

        sentiment_results = analyze_sentiment(news_data)
        comparative_analysis = generate_comparative_analysis(sentiment_results)

        for news in sentiment_results:
            st.write(f"### 📰 {news['title']}")
            st.write(f"📌 **Summary:** {news['summary']}")
            st.write(f"📊 **Sentiment:** {news['sentiment']}")
            st.write(f"🔗 [Read More]({news['link']})")
            st.write("---")

        st.write("## 📈 Sentiment Analysis Summary")
        st.write(comparative_analysis)

        tts_text = f"The company {company_name} has {comparative_analysis['Positive']} positive, {comparative_analysis['Negative']} negative, and {comparative_analysis['Neutral']} neutral news articles."
        audio_file = text_to_speech(tts_text)
        st.audio(audio_file)

if __name__ == "__main__":
    main()
