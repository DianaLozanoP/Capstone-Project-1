from unittest import TestCase
from flask import session, make_response, jsonify, g
from models import db, User, Budget, Wallets, Transactions
import os
# Use database for testing
os.environ['DATABASE_URL'] = "postgresql:///budgetbase-test2"
from app import app
app.config['SQLALCHEMY_ECHO'] = False


# Allow flask errors to be errors, rather than showing the HTML page with error info
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED']=False

db.drop_all()
db.create_all()

USER_DATA_1 ={
    "username": "Alberto", 
    "password": "abc123456", 
    "email": "alberto123@gmail.com"
}

USER_DATA_2 ={
    "username": "Praxal", 
    "password": "abc123456", 
    "email": "praxal123@gmail.com"
}

USER_DATA_3 ={
    "username": "Viviana", 
    "password": "abc123456", 
    "email": "viviana123@gmail.com"
}

USER_DATA_4 ={
    "username": "Blueberry", 
    "password": "abc123456", 
    "email": "blueberry123@gmail.com"
}

class BudgetsViewsTestCase(TestCase):
        """Tests for views of Budgets"""    
        def setUp(self):
            with app.test_client() as client:
                """Sign Up"""
                resp = client.post("/signup", data=USER_DATA_1, follow_redirects=True)
                html = resp.get_data(as_text=True)
    
                self.assertIn('Welcome back, Alberto!', html)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(User.query.first().email, USER_DATA_1["email"] )
                self.assertEqual(session['curr_user'], User.query.first().id)
        
        def tearDown(self):
            """Log out"""
            user = User.query.filter_by(email = USER_DATA_1["email"]).first()
            db.session.delete(user.wallet[0])
            db.session.delete(user)
            db.session.commit()
    
        def test_wallet(self):
            user = User.query.first()
            with app.test_client() as client:
                    #new session, so log in with user created 
                    login = client.post('/login', data=USER_DATA_1)
                    #go to the wallet page
                    resp = client.get(f'/wallet/{user.id}',follow_redirects=True)
                    html = resp.get_data(as_text=True)

                    self.assertEqual(user.wallet[0].amt, 0)
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn(f'Hi {user.username}', html)
                    self.assertIn('Add money into your wallet', html)

                    #add money into the wallet
                    resp2 = client.post(f'/wallet/{user.id}',data={"amt": 200},follow_redirects=True)
                    html2 = resp2.get_data(as_text=True)
                    
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn('200 was added to your wallet.', html2)

        def test_budgets(self):
            user = User.query.first()
            with app.test_client() as client:
                #new session, so log in with user created 
                login = client.post('/login', data=USER_DATA_1)
                resp = client.get(f"/budgets/{user.id}", follow_redirects=True)
                html = resp.get_data(as_text=True)
    
                self.assertEqual(resp.status_code, 200)
                self.assertIn('You have not created any budgets', html)

                #create a new budget
                resp2 =client.post(f"/budgets/{user.id}",data={'name':'Trip to Quebec'}, follow_redirects=True)
                html2 = resp2.get_data(as_text=True)
                self.assertEqual(resp2.status_code, 200)
                self.assertIn('These are your current budgets', html2)
        
        def test_transactions(self):
            user = User.query.first()
            with app.test_client() as client:
                #new session, so log in with user created 
                login = client.post('/login', data=USER_DATA_1)
                resp = client.get(f"/transactions/{user.id}", follow_redirects=True)
                html = resp.get_data(as_text=True)

              
                self.assertEqual(resp.status_code, 200)
                self.assertIn(' <p>You have not done any transactions.</p>',html)

                #select budget to add transaction
                resp2 = client.post(f"/transactions/{user.id}", data={'budget_id':user.budgets},follow_redirects=True)
                html2 = resp2.get_data(as_text=True)
                
                self.assertEqual(resp.status_code, 200)
                self.assertIn('<p>Choose from which budget this transaction belongs to</p>',html)
        
        def test_indexfunds(self):
            with app.test_client() as client:
                #new session, so log in with user created 
                login = client.post('/login', data=USER_DATA_1)
                resp = client.get(f"/IndexFunds")
    
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Advancements in current technology have significantly streamlined the process of investing in company stocks',resp.data.decode('utf-8'))
    