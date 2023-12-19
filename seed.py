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
        fund_type = each['fund_type']
        performance_rating = each['performance_rating']
        risk_rating = each['risk_rating']
        new_mtfs = MutualFunds(ticker=ticker, name=name2, fund_type=fund_type,
                               performance_rating=performance_rating, risk_rating=risk_rating)
        db.session.add(new_mtfs)
        db.session.commit()
    return {"Answer": "The database was seeded"}
