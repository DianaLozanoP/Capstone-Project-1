from models import MutualFunds, ETFs, MutualFunds
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


def seedMTs(data):
    """Based on data received, enter it into the database"""
    list = data['result']
    for each in list['list']:
        ticker = each['symbol']
        name = each['name']
        name2 = name.replace(';', '')
        country = each['country']
        new_mtfs = MutualFunds(ticker=ticker, name=name2, country=country)
        db.session.add(new_mtfs)
        db.session.commit()
    return {"Answer": "The database was seeded"}
