import httpx
import pandas as pd
import streamlit as st

API_KEY = st.secrets["GROK_API_KEY"]  # तुम्ही .streamlit/secrets.toml मध्ये ठेवा
API_URL = "https://api.grok.com/v1/chat/completions"  # हे खरं endpoint असलं पाहिजे

def extract_financial_data(text):
    prompt = get_prompt_financial() + text

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-1",  # खरं मॉडेल नाव इथे द्या
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = httpx.post(API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        data = eval(content) if isinstance(content, str) else content
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except Exception as e:
        st.error(f"❌ API Error: {e}")
        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })

def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (EPS)
from the following news article. If any data is missing, return an empty string for that field.
Then use your general knowledge to retrieve a stock symbol. Respond ONLY in valid JSON like:
{
    "Company Name": "Tesla",
    "Stock Symbol": "TSLA",
    "Revenue": "30 billion",
    "Net Income": "4.5 billion",
    "EPS": "2.3"
}
News Article:
============
'''
