from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])


class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])


class EditWallet(FlaskForm):
    """Wallet form"""
    amt = IntegerField('Amount to be added', validators=[DataRequired()])


class AddBudget(FlaskForm):
    """Budget Form"""
    name = StringField('Name', validators=[DataRequired()])


class AddCategory(FlaskForm):
    """Categories Form"""
    name = StringField('Category Name', validators=[DataRequired()])
    amt = IntegerField('Amount', validators=[DataRequired()])


class SelectBudget(FlaskForm):
    """Select the specific budget, to then enter the category"""
    budget_id = SelectField('Budgets')


class AddTransaction(FlaskForm):
    """Transaction form"""
    cat_id = SelectField('Category')
    amt = IntegerField('Amount spent', validators=[DataRequired()])
    description = StringField(
        'Description (optional)', validators=[Optional()])


class FilterETF(FlaskForm):
    """Filter the ETFs by different country"""
    country = SelectField("Filter by country")


class filterMutualFunds(FlaskForm):
    """Filter country for Mutual Funds"""
    performance_rating = SelectField("Filter by performance rating")
