import streamlit as st
from utils.api_connectors import (
    get_binance_price,
    get_cryptopanic_news,
    get_coinmarketcap_data,
    convert_currency,
    get_token_ticker  # Импортируем функцию из api_connectors
)
from utils.ai_handler import generate_response

# Инициализация интерфейса
st.set_page_config(page_title="AI Crypto Assistant", layout="wide")
st.title("📊 AI Crypto Assistant")

# Пользовательский ввод
query = st.text_input("Ask about any Top 50 crypto (e.g., Bitcoin or SOL):", 
                     help="Supports all cryptocurrencies in Top 50 by market cap")

# Блок конвертации валют
with st.expander("💱 Currency Conversion", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        convert_to = st.selectbox("Target currency:", ["USD", "EUR", "BTC", "ETH"])
    with col2:
        convert_amount = st.number_input("Amount to convert:", 
                                       min_value=0.01, 
                                       value=1.0,
                                       step=0.1)

if query:
    with st.spinner("🔍 Fetching latest crypto data..."):
        # Определяем токен через функцию из api_connectors
        token = get_token_ticker(query)
        
        if not token:
            st.error("❌ This cryptocurrency is not in Top 50. Try 'Bitcoin' or 'Ethereum'.")
            st.stop()

        # Получаем данные
        price = get_binance_price(token)
        news = get_cryptopanic_news(token)
        market_data = get_coinmarketcap_data(token)
        
        # Обработка ошибок данных
        if None in [price, news, market_data]:
            st.error("⚠️ API request failed. Please check your connection and try again.")
            st.stop()

        # Конвертация валют (если выбрано не USD)
        if convert_to != "USD":
            converted = convert_currency(token, convert_to, convert_amount)
            if converted is not None:
                st.success(f"**{convert_amount} {token} = {converted:.6f} {convert_to}**")
            else:
                st.warning(f"Conversion {token} → {convert_to} is not supported by Binance")

        # Генерация ответа
        response = generate_response(
            query=query,
            price=price,
            news=news,
            market_data=market_data,
        )
        
        # Вывод результата
        st.markdown("---")
        st.markdown(response)
        st.markdown("---")
        
        # Отладочная информация (можно скрыть)
        with st.expander("Debug Info"):
            st.json({
                "token": token,
                "price": price,
                "convert_to": convert_to,
                "converted": converted if convert_to != "USD" else None
            })