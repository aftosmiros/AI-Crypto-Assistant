import streamlit as st
from utils.api_connectors import *
from utils.ai_handler import generate_response

st.title("AI Crypto Assistant")
query = st.text_input("Ask about any crypto (e.g., Ethereum):")

if query:
    with st.spinner("Fetching data..."):  # Индикатор загрузки
        # Определяем токен (простой вариант)
        token = "ETH" if "ethereum" in query.lower() else "BTC"  # TODO: Заменить на более умный парсинг
        
        # Получаем данные
        price = get_binance_price(token)
        news = get_cryptopanic_news(token)
        market_data = get_coinmarketcap_data(token)
        
        # Проверяем, что все данные получены
        if None in [price, news, market_data]:
            st.error("Failed to fetch data. Please try again later.")
        else:
            # Генерируем ответ
            response = generate_response(
                query=query,
                price=price,
                news=news,  
                market_data=market_data,
            )

            st.success(response)