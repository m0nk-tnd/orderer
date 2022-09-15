from os import getenv


class Config:
    RATE_SERVER = getenv("RATE_SERVER", "https://www.cbr.ru/scripts/XML_daily.asp")
    SPREADSHEET_ID = getenv("SPREADSHEET_ID", "")
    RANGE_NAME = getenv("RANGE_NAME", "A2:E")
    PROGRAM_DELAY_SEC = int(getenv("PROGRAM_DELAY_SEC", 30))
    CURRENCY_SEARCH_STRING = getenv("CURRENCY_SEARCH_STRING", "Valute[@ID='R01235']")
    API_KEY = getenv("API_KEY", "333")
    BOT_TOKEN = getenv("BOT_TOKEN", "333")
    CHAT_ID = getenv("CHAT_ID", "333")

    DB_NAME = getenv("DB_NAME", "333")
    DB_USER = getenv("DB_USER", "333")
    DB_PASSWORD = getenv("DB_PASSWORD", "333")
    DB_HOST = getenv("DB_HOST", "db1")
    DB_PORT = int(getenv("DB_PORT", 5555))

    @classmethod
    def db_uri(cls) -> str:
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{str(cls.DB_PORT)}/{cls.DB_NAME}"
