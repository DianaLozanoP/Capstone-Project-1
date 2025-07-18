"""SQLAlchemy models for Gizmo Money"""

# import SQLAlchemy(Python SQL toolkit, Obj.Relational Mapper)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from flask_bcrypt import Bcrypt
from datetime import datetime


db = SQLAlchemy()
bcrypt = Bcrypt()


class Budget(db.Model):
    """model for SQLAlchemy. Budgets table"""

    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    total_amt = db.Column(db.Integer(), nullable=False, default=0)
    categories = db.relationship(
        'Category', cascade='all, delete-orphan', backref='budget')
    transactions = db.relationship(
        'Transactions', cascade='all, delete-orphan', backref='budget')


class Category(db.Model):
    """model for SQLAlchemy. Categories table"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_id = db.Column(db.Integer, db.ForeignKey(
        'budgets.id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    amt = db.Column(db.Integer(), nullable=False)
    amt_spent = db.Column(db.Integer(), default=0)
    transactions = db.relationship(
        'Transactions', cascade='all, delete-orphan', backref='category')


class Transactions(db.Model):
    """model for SQLAlchemy. Categories table"""

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey(
        'budgets.id'), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey(
        'wallets.id'), nullable=False)
    amt = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Wallets(db.Model):
    """model for SQLAlchemy. Wallets table"""

    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), nullable=False)
    amt = db.Column(db.Integer, nullable=False, default=0)
    transactions = db.relationship(Transactions)


class MutualFunds(db.Model):
    """model for SQLAlchemy. Mutual Funds table"""

    __tablename__ = 'mutualfunds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    fund_type = db.Column(db.String())
    performance_rating = db.Column(db.Integer())
    risk_rating = db.Column(db.Integer())


class ETFs(db.Model):
    """model for SQLAlchemy. ETFs table"""

    __tablename__ = 'etfs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=True)
    market = db.Column(db.String(), nullable=True)


class MFUser(db.Model):
    """model for SQLAlchemy. Mutual Funds-User following table"""

    __tablename__ = 'followmt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mutfund_followed = db.Column(db.Integer, db.ForeignKey(
        'mutualfunds.id', ondelete='cascade'))
    user_following = db.Column(
        db.Integer,  db.ForeignKey('users.id', ondelete="cascade"))


class ETFUser(db.Model):
    """Model for SQLAlchemy. ETFs-User following table"""

    __tablename__ = 'followetf'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    etf_followed = db.Column(db.Integer, db.ForeignKey(
        'etfs.id', ondelete='cascade'))
    user_following = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))


class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    wallet = db.relationship('Wallets', cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', cascade='all, delete-orphan')
    mt_following = db.relationship(MutualFunds, secondary='followmt', primaryjoin=(
        'MFUser.user_following == User.id'), secondaryjoin=(MFUser.mutfund_followed == MutualFunds.id))
    etf_following = db.relationship(ETFs, secondary='followetf', primaryjoin=(
        'ETFUser.user_following == User.id'), secondaryjoin=(ETFUser.etf_followed == ETFs.id))

    @classmethod
    def signup(cls, username, password, email):
        """Register a user, hash their password, create a wallet, and return the user."""
        hashed = bcrypt.generate_password_hash(str(password)).decode('utf8')
        user = cls(username=username, password=hashed, email=email)
        
        db.session.add(user)
        db.session.flush()  # Flush assigns an ID to the user before committing
    
        # Automatically create wallet for the new user
        wallet = Wallets(user_id=user.id, amt=0)
        db.session.add(wallet)
    
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Validate that user & password are correct.
        Return USER info is valid; else return FALSE."""
        # check for user's info into database
        u = User.query.filter_by(email=email).first()
        psw = str(password)
        if u and bcrypt.check_password_hash(u.password, psw):
            return u
        else:
            return False
           

def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)
