# News Sentiment Analyzer

📌 Overview
The **News Sentiment Analyzer** is a Streamlit-based web application that fetches news articles about a company, analyzes their sentiment, and provides a summary using Text-to-Speech (TTS) technology. The project integrates **web scraping, sentiment analysis, and speech synthesis** to offer a seamless experience for users to gauge a company's public perception.

---

🚀 Project Setup

1️⃣ Clone the Repository**
```bash
git clone https://huggingface.co/spaces/kt2527/news-sentiment-analyzer
cd news-sentiment
```

2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ Run the Application**
```bash
streamlit run app.py
```

---

-> 🧠 Model Details

Summarization Model
The app scrapes news articles from **Google News RSS** and extracts summaries using **BeautifulSoup**.

-> Sentiment Analysis Model**
- Uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** from `vaderSentiment`.
- Determines sentiment polarity as **Positive, Negative, or Neutral** based on article summaries.

-> Text-to-Speech (TTS) Model**
- **Bark AI** is used for converting text summaries into Hindi speech.
- The audio is synthesized and saved as a `.wav` file for playback.

---

-> 🛠️ API Development

The application does not provide a REST API but functions as an interactive **Streamlit** UI. However, the following core functions serve as internal APIs:

1. extract_news(company_name) → Fetches news articles using Google News RSS.
2. analyze_sentiment(news_data) → Performs sentiment analysis on extracted news.
3. generate_comparative_analysis(sentiment_results) → Aggregates sentiment statistics.
4. text_to_speech(text) → Converts text into Hindi speech.

-> Accessing APIs via Postman or Other Tools**
If needed, the backend logic can be wrapped into a **Flask** or **FastAPI** server for API-based access.

---

-> 🌐 API Usage

-> Third-Party APIs Used
- Google News RSS : Fetches news articles based on company name 
- Bark AI (Text-to-Speech) : Generates speech output for summaries 

-> Integration Details
-> Google News RSS: The application sends an HTTP GET request to `https://news.google.com/rss/search?q=<company_name>` to extract news articles.
- **Bark AI:** Uses the `generate_audio()` function to convert text into speech.

---

-> 📌 Assumptions & Limitations

-> Assumptions
✔ The input company name is correctly spelled and widely covered in news sources.
✔ The user has an active internet connection for fetching news.
✔ Sentiment analysis using VADER is suitable for short-form news summaries.
✔ Bark AI supports Hindi TTS generation without additional fine-tuning.

-> **Limitations**
❌ Google News RSS may not return **all relevant** articles, limiting sentiment analysis coverage.
❌ Sentiment analysis with VADER works well for **English text** but might misclassify complex sentiments.
❌ Bark AI **Hindi TTS** output quality might be inconsistent for certain phrases.

---

-> 🔗 Deployment & Access
https://huggingface.co/spaces/kt2527/news-sentiment-analyzer

👨‍💻 **Developed by**: Koustubh Trivedi | 📅 **Date**: March 2025

