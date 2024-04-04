from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22663326"))
    API_HASH = getenv("API_HASH", "927e822ca6e854d8b7369c72ab9506e4")
    BOT_TOKEN = getenv("BOT_TOKEN", "6756845327:AAGwyRCE2YlVZQihOhJzbWj2qz7J7rx4dU8")
    FSUB = getenv("FSUB", "your channel username")
    CHID = int(getenv("CHID", "your channel id"))
    SUDO = list(map(int, getenv("SUDO").split()))
    MONGO_URI = getenv("mongodb+srv://tigamow711:s0cUEhrE1Jb5Iehs@vsfsb.pb89igt.mongodb.net/", "mongodb url")
    
cfg = Config()
