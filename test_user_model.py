"""User model tests"""

# run test
# python -m unittest test_user_model.py



import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User
# before we import app, let's set an environmental variable
os.environ['DATABASE_URL'] = "postgresql:///budgetbase-test"

from app import app
db.create_all()


class UserModelTestCase(TestCase):
    """Test"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "password8", "email1@gmail.com")
        u1_id = 33
        u1.id = u1_id

        u2 = User.signup("test2", "password8", "email2@gmail.com")
        u2_id = 34
        u2.id = u2_id

        db.session.commit()

        u1 = User.query.get(u1_id)
        u2 = User.query.get(u2_id)

        self.u1 = u1
        self.uid1 = u1_id

        self.u2 = u2
        self.uid2 = u2_id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_signup(self):
        """Test basic model"""
        u = User.signup(username='testuser',
                        email='testuser@gmail.com', password='123456ABC')
        u_id = 35
        u.id = u_id
        db.session.commit()

        u = User.query.get(u_id)
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.email, "testuser@gmail.com")
        # Check that the password is a bcrypt string
        self.assertTrue(u.password.startswith('$2b$'))

    def test_invalid_username(self):
        """Testing sign up with invdalid username"""
        u = User.signup(None, "abc123456", "usertest3@gmail.com")
        u_id = 99
        u.id = u_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email(self):
        """Testing sign up with invalid email"""
        u = User.signup("usertest123", "abc123456", None)
        u_id = 123
        u.id = u_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password(self):
        """Testing sign up with invalid password"""
        User.signup("usertest369", None, "user8@yahoo.com")
        with self.assertRaises(ValueError) as context:
            db.session.commit()

    def test_authentication(self):
        """Testing that authentication works"""
        u = User.signup("usertest8", "abc123456", "usertest8@gmail.com")
        u_id = 369
        u.id = u_id
        db.session.add(u)
        db.session.commit()

        User.authenticate('usertest8@gmail.com', 'abc123456')
        user = User.query.get(369)
        self.assertEqual(User.authenticate(
            'usertest8@gmail.com', 'abc123456'), user)

    def test_fail_authentication(self):
        """Testing when username is not valid"""
        self.assertFalse(User.authenticate('notauser@gmail.com', 'abc123'))

    def test_fail_authentication(self):
        """Testing when password is not valid"""
        u = User.signup('usertest15', 'abc123456', 'user15@yahoo.com')
        u_id = 115
        u.id = u_id
        db.session.add(u)
        db.session.commit()
        self.assertFalse(User.authenticate('usertest15', '000000000'))
