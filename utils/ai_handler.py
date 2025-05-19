from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Optional, Dict, List, Union

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(
    query: str,
    price: Optional[float],
    news: List[Dict],
    market_data: Dict[str, Union[float, int, str]],
    converted: Optional[float] = None,
    convert_to: str = "USD",
    convert_amount: float = 1.0
) -> str:
    """
    Генерирует ответ с учетом конвертации валют и рыночных данных
    
    Параметры:
        query: Пользовательский запрос
        price: Текущая цена
        news: Список новостей
        market_data: Рыночные данные (capitalization, rank)
        converted: Конвертированная сумма
        convert_to: Валюта конвертации
        convert_amount: Исходное количество
    """
    # Обработка новостей
    news_text = "\n".join([f"- {item.get('title', 'No title')} (Source: CryptoPanic)" 
                          for item in news[:3]]) if news else "No recent news available"
    
    # Форматирование чисел
    def format_value(value, is_currency=True):
        if value is None:
            return "N/A"
        if isinstance(value, str):
            return value
        return f"${value:,.2f}" if is_currency else f"{value:,}"

    # Основные данные
    market_cap = market_data.get('market_cap')
    rank = market_data.get('rank', 'N/A')
    
    # Формируем базовый ответ
    base_response = f"""
    📊 Crypto Assistant Response 📊
    
    🔹 User Question: "{query}"
    
    💰 Current Price: {format_value(price)}
    📈 Market Cap: {format_value(market_cap)}
    🏆 Rank: #{rank}
    
    📰 Latest News:
    {news_text}
    """

    # Добавляем конвертацию если есть
    if converted and convert_to != "USD":
        conversion_text = (
            f"\n💱 Conversion: {convert_amount} {market_data.get('symbol', 'coin')} "
            f"= {format_value(converted)} {convert_to}"
        )
        base_response += conversion_text

    # Если OpenAI доступен
    try:
        prompt = f"""
        Сгенерируй краткий ответ на вопрос о криптовалюте используя эти данные:
        
        {base_response}
        
        Ответ должен быть:
        - На языке оригинала вопроса
        - Максимально информативным
        - С выделением ключевых цифр
        - Без технических деталей запроса
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.5
        )
        return response.choices[0].message.content
        
    except Exception as e:
        # Fallback если OpenAI недоступен
        return base_response + "\n\nℹ️ AI summary is currently unavailable."