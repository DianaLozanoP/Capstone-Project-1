from models import MutualFunds, ETFs, MutualFunds
from app import db


def seedETFs(data):
    """Based on data received, enter it into the database"""
    try:
    # your existing code for adding and committing to the database
        etfs_to_add =[]
        for each in data['data']:
            ticker = each['symbol']
            name = each['name']
            country  = each["country"]
            market = each["mic_code"]
            name2 = name.replace(';', "")
            name3 =name2.replace("-", "")
            new_etf = ETFs(ticker=ticker, name=name3,
                           country=country, market=market)
            etfs_to_add.append(new_etf)
        db.session.add_all(etfs_to_add)
        db.session.commit()
        
        return {"Answer": "The database was seeded"}
        
    except Exception as e:
       db.session.rollback()  # Rollback changes in case of an error
       return {"Error": f"Failed to seed data. Error: {str(e)}"}
 


def seedMTs(data):
    """Based on data received, enter it into the database"""
    list = data['result']
    for each in list['list']:
        ticker = each['symbol']
        name = each['name']
        name2 = name.replace(';', '')
        name3 =name2.replace("-", "")
        fund_type = each['fund_type']
        performance_rating = each['performance_rating']
        risk_rating = each['risk_rating']
        new_mtfs = MutualFunds(ticker=ticker, name=name3, fund_type=fund_type,
                               performance_rating=performance_rating, risk_rating=risk_rating)
        db.session.add(new_mtfs)
        db.session.commit()
    return {"Answer": "The database was seeded"}
