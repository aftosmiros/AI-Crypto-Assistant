# AI-Crypto-Assistant

AI_Crypto_Assistant/
├── .env                    # Для хранения API-ключей
├── README.md               # Документация (описание, примеры, скриншоты)
├── app.py                  # Основной код (Streamlit для интерфейса + логика)
├── requirements.txt        # Зависимости Python
├── utils/
│   ├── api_connectors.py   # Подключение к API (Binance, CoinMarketCap, CryptoPanic)
│   ├── ai_handler.py       # Обработка запросов через GPT
│   └── data_aggregator.py  # Агрегация данных из API
└── assets/                 # Папка для скриншотов/GIF (для README)