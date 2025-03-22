import os
import streamlit as st
import json
import requests
import matplotlib.pyplot as plt
import pandas as pd
from utils import extract_news, analyze_sentiment, generate_comparative_analysis, text_to_speech

st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")

st.title("📊 Company News Sentiment Analyzer")

# Function to process news sentiment analysis
def analyze_news(company_name):
    news_data = extract_news(company_name)
    
    if not news_data:
        return {"error": "No relevant news found. Try another company."}

    sentiment_results = analyze_sentiment(news_data)
    comparative_analysis = generate_comparative_analysis(sentiment_results)

    tts_text = f"The company {company_name} has {comparative_analysis['Positive']} positive, {comparative_analysis['Negative']} negative, and {comparative_analysis['Neutral']} neutral news articles."
    tts_file = text_to_speech(tts_text)

    return {
        "company": company_name,
        "articles": sentiment_results,
        "comparative_analysis": comparative_analysis,
        "tts_audio": tts_file
    }

# Streamlit UI
st.write("## Analyze Company Sentiment")
company_name = st.text_input("Enter Company Name")

if st.button("Analyze"):
    response = analyze_news(company_name)

    if "error" in response:
        st.warning(response["error"])
    else:
        for news in response["articles"]:
            st.write(f"### 📰 {news['title']}")
            st.write(f"📌 **Summary:** {news['summary']}")
            st.write(f"📊 **Sentiment:** {news['sentiment']}")
            st.write(f"🔗 [Read More]({news['link']})")
            st.write("---")

        st.write("## 📈 Sentiment Analysis Summary")
        st.write(response["comparative_analysis"])

        tts_audio_path = response["tts_audio"]
        if os.path.exists(tts_audio_path):
            st.write("## 🔊 Hindi TTS Summary")
            st.audio(tts_audio_path)
        else:
            st.warning("TTS audio not generated. Try again.")

# Compare Two Companies
st.write("### Compare Two Companies")
company1 = st.text_input("Enter First Company Name")
company2 = st.text_input("Enter Second Company Name")

if st.button("Compare Sentiment"):
    news1 = extract_news(company1)
    news2 = extract_news(company2)

    if not news1 or not news2:
        st.warning("News not found for one or both companies.")
    else:
        sentiment1 = generate_comparative_analysis(analyze_sentiment(news1))
        sentiment2 = generate_comparative_analysis(analyze_sentiment(news2))
        st.write("### Sentiment Comparison")
        st.write({company1: sentiment1, company2: sentiment2})
