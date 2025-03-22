from fastapi import FastAPI
from utils import extract_news, analyze_sentiment, generate_comparative_analysis, text_to_speech

app = FastAPI()

@app.get("/news/")
def get_news(company_name: str):
    """Fetches news articles, performs sentiment analysis, and generates TTS."""
    news_data = extract_news(company_name)
    
    if not news_data:
        return {"error": "No relevant news found. Try another company."}

    sentiment_results = analyze_sentiment(news_data)
    comparative_analysis = generate_comparative_analysis(sentiment_results)

    # Generate TTS summary
    tts_text = f"The company {company_name} has {comparative_analysis['Positive']} positive, {comparative_analysis['Negative']} negative, and {comparative_analysis['Neutral']} neutral news articles."
    tts_file = text_to_speech(tts_text)

    return {
        "company": company_name,
        "articles": sentiment_results,
        "comparative_analysis": comparative_analysis,
        "tts_audio": tts_file
    }

@app.get("/compare/")
def compare_companies(company1: str, company2: str):
    """Compares sentiment analysis between two companies."""
    news1 = extract_news(company1)
    news2 = extract_news(company2)

    if not news1 or not news2:
        return {"error": "News not found for one or both companies."}

    sentiment1 = generate_comparative_analysis(analyze_sentiment(news1))
    sentiment2 = generate_comparative_analysis(analyze_sentiment(news2))

    return {
        company1: sentiment1,
        company2: sentiment2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
