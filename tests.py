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
                self.assertEqual(session['curr_user'], 1)
        
        def tearDown(self):
            """Log out"""
            with app.test_client() as client:
                resp = client.get("/logout", follow_redirects=True)
                html = resp.get_data(as_text=True)
    
                self.assertIn(' <div class="alert alert-success">You have logged out</div>', html)
                self.assertEqual(resp.status_code, 200)
            
            
    
        # def test_login(self):
        #      with app.test_client() as client:
        #         resp = client.post('/login', data=USER_DATA_1, follow_redirects=True)
        #         html = resp.get_data(as_text=True)
                  
        #         user = User.query.all()
               
        #              #           user = User.authenticate( 
        # # "alberto123@gmail.com", "abc123456")
        #         import pdb
        #         pdb.set_trace()
        #         self.assertEqual(user, False)
        # #         self.assertEqual(resp.status_code, 200)
        # #         self.assertIn('Welcome back, Alberto!', html)
    
    
        def test_wallet(self):
            user = User.query.first()
            with app.test_client() as client:
                    resp = client.get(f'/wallet/{user.id}',follow_redirects=True)
                    html = resp.get_data(as_text=True)
                    with client.session_transaction() as sess:
                         sess["curr_user"] = 1
                    self.assertEqual(g.user, 1)
                    self.assertEqual(resp.status_code, 200)
                    self.assertEqual(user.username, "Alberto")
                    self.assertIn(f'Hi {user.username}', html)
                    self.assertIn('Add money into your wallet', html)
        
        # def test_budgets(self):
        #     with app.test_client() as client:
        #         resp = client.get(f"/budgets/{self.user.id}")
    
        #         self.assertEqual(resp.status_code, 302)
        #         self.assertIn('You have not created any budgets', resp.data.decode('utf-8'))
        
        # def test_transactions(self):
        #     with app.test_client() as client:
        #         resp = client.get(f"/transactions/{self.user.id}")
    
        #         self.assertEqual(resp.status_code, 200)
        #         self.assertIn('You have not done any  transactions',resp.data.decode('utf-8'))
        
        # def test_indexfunds(self):
        #     with app.test_client() as client:
        #         resp = client.get(f"/IndexFunds")
    
        #         self.assertEqual(resp.status_code, 200)
        #         self.assertIn('Advancements in current technology have significantly streamlined the process of investing in company stocks',resp.data.decode('utf-8'))
    