import httpx
import pandas as pd
import streamlit as st

def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    try:
        response = httpx.post(
            "https://api.grok.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.secrets['GROK_API_KEY']}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-1",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        content = response.json()["choices"][0]["message"]["content"]
        data = eval(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except Exception as e:
        st.error(f"❌ Error from Grok: {str(e)}")
        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })

def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid Python dictionary like this: 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''
