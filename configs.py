from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22663326"))
    API_HASH = getenv("API_HASH", "927e822ca6e854d8b7369c72ab9506e4")
    BOT_TOKEN = getenv("BOT_TOKEN", "6756845327:AAGwyRCE2YlVZQihOhJzbWj2qz7J7rx4dU8")
    FSUB = getenv("FSUB", "PremiumCheapDealsOffers")
    CHID = int(getenv("CHID", "-1002025332256"))
    SUDO = list(map(int, getenv("1654334233", "").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://tigamow711:s0cUEhrE1Jb5Iehs@vsfsb.pb89igt.mongodb.net/")
    
cfg = Config()
