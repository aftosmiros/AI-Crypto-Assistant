# AI Crypto Assistant

[Demo Screenshot](./assets/home.png)

## Description
AI Crypto Assistant is a real-time cryptocurrency information tool that provides data for top 50 coins by market capitalization. It integrates Binance (prices), CoinMarketCap (market data), CryptoPanic (news), and OpenAI (response generation).

## Features
- Real-time price checking
- Market cap and ranking data
- Latest cryptocurrency news
- Cross-currency conversion
- AI-powered response generation
- Supports top 50 cryptocurrencies

## Requirements
- Python 3.10+
- API keys from:
  - [Binance](https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072)
  - [CoinMarketCap](https://coinmarketcap.com/api/)
  - [CryptoPanic](https://cryptopanic.com/developers/api/)
  - [OpenAI](https://platform.openai.com/api-keys)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-crypto-assistant.git
   cd ai-crypto-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   - Rename `.env.example` to `.env`
   - Add your API keys:
     ```ini
     BINANCE_API_KEY=your_api_key
     BINANCE_SECRET_KEY=your_secret_key
     COINMARKETCAP_API_KEY=your_api_key
     CRYPTO_PANIC_API_KEY=your_api_key
     OPENAI_API_KEY=your_api_key
     ```

## Usage
1. Launch the application:
   ```bash
   streamlit run app.py
   ```

2. Enter queries about cryptocurrencies:
   ```
   Supported queries:
   - Price checks (e.g., "Bitcoin price")
   - Market data (e.g., "Solana market cap")
   - News requests (e.g., "Ethereum news")
   - Currency conversion (e.g., "Convert 1 BTC to EUR")
   ```

3. Use the conversion panel:
   ```
   1. Select target currency (USD/EUR/BTC/ETH)
   2. Enter amount
   3. View real-time conversion
   ```
   [Convert Screenshot](./assets/convert.png)

## Supported Cryptocurrencies
Top 50 coins by market cap including:
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Solana (SOL)
- Ripple (XRP)
- [Full list available](./assets/top50_coins.txt)

## Examples
| Query | Response Contains |
|-------|-------------------|
| "Bitcoin price" | Current BTC price in USD |
| "Ethereum news" | 3 latest ETH news items |
| "Convert 1 SOL to EUR" | Euro equivalent |
| "BNB market cap" | Market capitalization and rank |

![Interface Example](./assets/ai-crypto-assistant_query.png)

## Project Structure
```
ai-crypto-assistant/
├── app.py                # Main application
├── utils/
│   ├── api_connectors.py # API integrations
│   └── ai_handler.py     # Response generation
├── assets/               # Media files
│   ├── demo.gif          # Screen recording
│   └── example.png       # Interface screenshot
├── .env                  # API keys (ignored in git)
├── requirements.txt      # Python dependencies
└── LICENSE               # MIT License
```

## API Reference
| Service | Purpose | Rate Limits |
|---------|---------|-------------|
| Binance | Price data | 1200 req/min |
| CoinMarketCap | Market data | 333 req/day |
| CryptoPanic | News | 100 req/day |
| OpenAI | AI responses | Depends on plan |

## License
This project is licensed under the [MIT License](./LICENSE).

## Authors
- [Miras (aftosmiros)](https://github.com/aftosmiros)
- [Nurkassym (abdaber)](https://github.com/abdaber)
