from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(query, price, news, market_data):
    # Проверка и обработка входных данных
    if not news:
        news = [{"title": "No recent news available"}]
    
    try:
        # Форматируем новости
        news_text = "\n".join([f"- {item.get('title', 'No title')} (Source: CryptoPanic)" 
                             for item in news[:3]])
        
        # Форматируем рыночные данные с проверкой
        market_cap = market_data.get('market_cap', 'N/A')
        rank = market_data.get('rank', 'N/A')
        
        market_text = f"""
        Price: ${price if price else 'N/A'} (Binance)
        Market Cap: ${market_cap:,} (CoinMarketCap)
        Rank: #{rank}
        """
        
        # Генерируем промпт
        prompt = f"""
        User question: {query}
        
        Market data:
        {market_text.strip()}
        
        Latest news:
        {news_text}
        
        Please provide a concise summary of this information.
        """
        
        # Запрос к OpenAI с обработкой ошибок
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Fallback response если OpenAI не работает
        return f"""
        User question: {query}
        
        Current price: ${price if price else 'N/A'}
        Market cap: ${market_cap:,}
        Rank: #{rank}
        
        Latest news:
        {news_text}
        """

# Пример использования:
# response = generate_response("What's the price of Bitcoin?", 50000, news_data, market_data)