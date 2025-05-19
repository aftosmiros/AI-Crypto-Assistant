import os
import requests
from dotenv import load_dotenv
from functools import lru_cache
from typing import Optional, Dict, List, Union

load_dotenv()

# Полный список топ-50 криптовалют (CoinMarketCap)
TOKEN_MAPPING = {
    # Топ-20
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "tether": "USDT",
    "binancecoin": "BNB",
    "solana": "SOL",
    "ripple": "XRP",
    "usd-coin": "USDC",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "shiba-inu": "SHIB",
    "avalanche": "AVAX",
    "chainlink": "LINK",
    "polkadot": "DOT",
    "tron": "TRX",
    "polygon": "MATIC",
    "toncoin": "TON",
    "bitcoin-cash": "BCH",
    "litecoin": "LTC",
    "uniswap": "UNI",
    "internet-computer": "ICP",
    
    # Топ 21-50
    "filecoin": "FIL",
    "stellar": "XLM",
    "vechain": "VET",
    "monero": "XMR",
    "cosmos": "ATOM",
    "aave": "AAVE",
    "algorand": "ALGO",
    "quant": "QNT",
    "near": "NEAR",
    "elrond": "EGLD",
    "theta": "THETA",
    "flow": "FLOW",
    "tezos": "XTZ",
    "axie-infinity": "AXS",
    "pancakeswap": "CAKE",
    "eos": "EOS",
    "iota": "MIOTA",
    "klaytn": "KLAY",
    "neo": "NEO",
    "curve-dao-token": "CRV",
    "kava": "KAVA",
    "waves": "WAVES",
    "zilliqa": "ZIL",
    "decentraland": "MANA",
    "the-sandbox": "SAND",
    "gala": "GALA",
    "enjin": "ENJ",
    "chiliz": "CHZ",
    "harmony": "ONE",
    "holo": "HOT"
}

@lru_cache(maxsize=100)
def get_token_ticker(query: str) -> Optional[str]:
    """
    Определяет тикер криптовалюты по названию с кэшированием результатов.
    
    Args:
        query: Запрос пользователя (например, "price of bitcoin")
    
    Returns:
        str: Тикер (например, "BTC") или None, если не найден
    """
    query_lower = query.lower()
    for name, ticker in TOKEN_MAPPING.items():
        if name in query_lower or ticker.lower() in query_lower:
            return ticker
    return None

@lru_cache(maxsize=100)
def get_binance_price(ticker: str) -> Optional[float]:
    """
    Получает цену криптовалюты с Binance API с кэшированием.
    Кэш сохраняется на 100 последних запросов.
    """
    try:
        if not ticker:
            return None
            
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"Binance API error: {e}")
        return None

@lru_cache(maxsize=50)
def get_coinmarketcap_data(ticker: str) -> Optional[Dict]:
    """
    Получает рыночные данные с CoinMarketCap API.
    Кэш обновляется при каждом новом тикере.
    """
    try:
        if not ticker:
            return None
            
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={ticker}"
        headers = {"X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_API_KEY")}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "symbol": ticker,
            "price": data["data"][ticker]["quote"]["USD"]["price"],
            "market_cap": data["data"][ticker]["quote"]["USD"]["market_cap"],
            "rank": data["data"][ticker]["cmc_rank"],
        }
    except Exception as e:
        print(f"CoinMarketCap API error: {e}")
        return None

@lru_cache(maxsize=50)
def get_cryptopanic_news(ticker: str) -> List[Dict]:
    """
    Получает последние новости с CryptoPanic.
    Кэш сохраняет 50 последних запросов.
    """
    try:
        if not ticker:
            return []
            
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={os.getenv('CRYPTO_PANIC_API_KEY')}&currencies={ticker}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"CryptoPanic API error: {e}")
        return []

@lru_cache(maxsize=100)
def convert_currency(from_ticker: str, to_ticker: str, amount: float = 1.0) -> Optional[float]:
    """
    Конвертирует сумму между криптовалютами/фиатами через Binance API.
    Поддерживаемые to_ticker: USD (через USDT), EUR, BTC, ETH и другие криптовалюты.
    """
    try:
        if not from_ticker:
            return None

        # Для фиатных валют (EUR) используем стабильные монеты как прокси
        if to_ticker in ["EUR"]:
            # Конвертируем сначала в USDT
            usdt_price = get_binance_price(from_ticker)  # from_ticker/USDT
            if not usdt_price:
                return None
            
            # Получаем курс EUR/USDT (обратная пара)
            url = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            eur_rate = float(response.json()["price"])
            
            return float(usdt_price) * amount / eur_rate
        
        # Для USD используем USDT
        elif to_ticker == "USD":
            price = get_binance_price(from_ticker)  # from_ticker/USDT
            return float(price) * amount if price else None
        
        # Для крипто-крипто пар (BTC, ETH и др.)
        else:
            # Проверяем обе возможные комбинации пар
            for pair in [f"{from_ticker}{to_ticker}", f"{to_ticker}{from_ticker}"]:
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    price = float(response.json()["price"])
                    return price * amount if pair.startswith(from_ticker) else (1/price) * amount
            
            return None
            
    except Exception as e:
        print(f"Currency conversion error: {e}")
        return None