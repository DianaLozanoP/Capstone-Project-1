from models import MutualFunds, ETFs
from app import db


def seedETFs(data):
    """Based on data received, enter it into the database"""

    for each in data['data']:
        ticker = each['symbol']
        name = each['name']
        country = each["country"]
        market = each["mic_code"]
        new_etf = ETFs(ticker=ticker, name=name,
                       country=country, market=market)
        db.session.add(new_etf)
        db.session.commit()
    return {"Answer": "The database was seeded"}
