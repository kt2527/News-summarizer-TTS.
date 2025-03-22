import os
import json
import requests
import torch
import soundfile as sf
from bark import generate_audio, preload_models
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def log_user_search(company_name):
    """Logs which companies users are searching for."""
    log_file = "search_logs.json"

    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = json.load(f)
        else:
            logs = {}

        logs[company_name] = logs.get(company_name, 0) + 1  # Count searches

        with open(log_file, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"Logging error: {e}")

def extract_news(company_name):
    """Extracts news articles from Google News RSS feed."""
    log_user_search(company_name)  # Log searches
    search_url = f"https://news.google.com/rss/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print("Error: Failed to fetch news.")
        return []

    try:
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")

        if not items:
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all("item")

        news_data = []
        for item in items[:10]:  
            title = item.find("title").text if item.find("title") else "No Title"
            summary = item.find("description").text if item.find("description") else "No Summary"
            summary = re.sub(r'<.*?>', '', summary)
            link = item.find("link").text if item.find("link") else "#"

            news_data.append({"title": title, "summary": summary, "link": link})

        return news_data

    except Exception as e:
        print("Error while parsing news:", str(e))
        return []

def analyze_sentiment(news_data):
    """Performs sentiment analysis on news summaries."""
    analyzer = SentimentIntensityAnalyzer()
    sentiment_results = []

    for news in news_data:
        score = analyzer.polarity_scores(news["summary"])
        sentiment = "Positive" if score['compound'] >= 0.05 else "Negative" if score['compound'] <= -0.05 else "Neutral"
        news["sentiment"] = sentiment
        sentiment_results.append(news)

    return sentiment_results

def generate_comparative_analysis(sentiment_results):
    """Generates sentiment summary across all news articles."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for result in sentiment_results:
        sentiment_counts[result["sentiment"]] += 1
    return sentiment_counts

def text_to_speech(text):
    """Convert text to Hindi speech using gTTS (faster alternative)."""
    tts = gTTS(text=text, lang="hi")
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path
