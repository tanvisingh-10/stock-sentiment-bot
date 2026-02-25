import requests
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

companies = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "State Bank of India": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Wipro": "WIPRO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Titan Company": "TITAN.NS",
    "Ultratech Cement": "ULTRACEMCO.NS",
    "Nestle India": "NESTLEIND.NS",
    "Power Grid": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "Tech Mahindra": "TECHM.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Grasim Industries": "GRASIM.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Dr Reddys Lab": "DRREDDY.NS",
    "Cipla": "CIPLA.NS",
    "Divis Lab": "DIVISLAB.NS",
    "Britannia": "BRITANNIA.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Coal India": "COALINDIA.NS",
    "ONGC": "ONGC.NS",
    "Tata Consumer": "TATACONSUM.NS",
    "Hindalco": "HINDALCO.NS",
    "UPL": "UPL.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "LTIMindtree": "LTIM.NS",
    "Tata Consultancy": "TCS.NS"
}

def get_top4_and_notify():
    analyzer = SentimentIntensityAnalyzer()
    results = []

    for name, ticker in companies.items():
        try:
            stock = yf.Ticker(ticker)
            news = stock.news[:5]
            
            total_score = 0
            count = 0
            
            for article in news:
                headline = article['content']['title']
                score = analyzer.polarity_scores(headline)
                total_score += score['compound']
                count += 1
            
            avg_score = total_score / count if count > 0 else 0
            
            if avg_score >= 0.15:
                signal = "🐂 Bullish"
            elif avg_score <= -0.05:
                signal = "🐻 Bearish"
            else:
                signal = "⚖️ Neutral"
            
            results.append({"company": name, "signal": signal, "score": round(avg_score, 3)})

        except Exception as e:
            continue

    results = sorted(results, key=lambda x: x['score'], reverse=True)
    top4 = results[:4]

    message = "📊 Tomorrow's Top 4 Stocks to Watch\n\n"
    for i, r in enumerate(top4):
        message += f"{i+1}. {r['signal']}  {r['company']}  (score: {r['score']})\n"
    message += "\n🤖 Powered by NSE Sentiment Bot"

    send_telegram(message)

get_top4_and_notify()
