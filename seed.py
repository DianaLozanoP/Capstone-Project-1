from models import MutualFunds, ETFs, MutualFunds
from app import db
from models import db, User, Budget, Category, Transactions, Wallets
from sqlalchemy.exc import IntegrityError

def seed_demo_user():
    """Seed the demo user if not already created."""
    demo = User.query.filter_by(username='demo').first()
    if not demo:
        demo = User.signup(username='demo', password='password', email='demo@example.com')
        db.session.add(demo)
        db.session.commit()
        print("Demo user created!")
    else:
        print("Demo user already exists.")
    return demo

def seed_demo_user_data():
    demo = User.query.filter_by(username='demo').first()

    if not demo:
        demo = User.signup(username='demo', password='password', email='demo@example.com')
        db.session.add(demo)
        db.session.commit()

    # Ensure demo has at least one wallet
    if not demo.wallets:
        wallet = Wallets(user_id=demo.id, amt=1000)
        db.session.add(wallet)
        db.session.commit()
    else:
        wallet = demo.wallet[0]

    # Ensure demo has a budget
    if not demo.budgets:
        budget = Budget(name='Monthly Budget', user_id=demo.id)
        db.session.add(budget)
        db.session.commit()
    else:
        budget = demo.budgets[0]

    # Create categories if none exist for the budget
    if not budget.categories:
        groceries = Category(name='Groceries', amt=300, budget_id=budget.id)
        transport = Category(name='Transport', amt=100, budget_id=budget.id)
        db.session.add_all([groceries, transport])
        db.session.commit()
    else:
        groceries = budget.categories[0]
        transport = budget.categories[1] if len(budget.categories) > 1 else None

    # Add demo transactions linked to wallet, budget, and categories
    t1 = Transactions(
        cat_id=groceries.id,
        budget_id=budget.id,
        wallet_id=wallet.id,
        amt=45,
        description='Bought vegetables'
    )

    t2 = Transactions(
        cat_id=transport.id,
        budget_id=budget.id,
        wallet_id=wallet.id,
        amt=20,
        description='Bus pass'
    )

    db.session.add_all([t1, t2])
    db.session.commit()




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

if __name__ == "__main__":
    seed_demo_user()
    seed_demo_user_data()
