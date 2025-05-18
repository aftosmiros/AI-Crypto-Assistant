import os
import requests
from dotenv import load_dotenv

# Словарь для преобразования названий токенов в тикеры (например, Ethereum -> ETH)
TOKEN_MAPPING = {
    "ethereum": "ETH",
    "bitcoin": "BTC",
    "solana": "SOL",
    # Добавьте остальные топ-50 монет
}

def get_token_ticker(token_name):
    """Преобразует название токена (например, 'Ethereum') в тикер ('ETH')."""
    return TOKEN_MAPPING.get(token_name.lower(), token_name.upper())

def get_binance_price(ticker):
    try:
        ticker = get_token_ticker(ticker)
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT"
        response = requests.get(url, timeout=5)  # Таймаут 5 секунд
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()["price"]
    except Exception as e:
        print(f"Binance API error: {e}")
        return None

def get_coinmarketcap_data(ticker):
    try:
        ticker = get_token_ticker(ticker)
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={ticker}"
        headers = {"X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Пример парсинга для CoinMarketCap (структура ответа сложная)
        return {
            "price": data["data"][ticker]["quote"]["USD"]["price"],
            "market_cap": data["data"][ticker]["quote"]["USD"]["market_cap"],
            "rank": data["data"][ticker]["cmc_rank"],
        }
    except Exception as e:
        print(f"CoinMarketCap API error: {e}")
        return None

def get_cryptopanic_news(ticker):
    try:
        ticker = get_token_ticker(ticker)
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={os.getenv('CRYPTO_PANIC_API_KEY')}&currencies={ticker}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()["results"]  # Возвращаем только список новостей
    except Exception as e:
        print(f"CryptoPanic API error: {e}")
        return None