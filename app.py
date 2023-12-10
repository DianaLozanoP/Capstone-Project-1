from flask import Flask, render_template, redirect, session, flash, g
from flask_debugtoolbar import DebugToolbarExtension
import os
from models import connect_db, db, User, Budget, Category, Transactions, Wallets, MutualFunds, ETFs
from forms import UserAddForm, LoginForm, AddBudget, AddCategory, EditWallet, SelectBudget, AddTransaction
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///budgetbase'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")


app.app_context().push()

connect_db(app)
# db.drop_all()
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.before_request
def add_user_to_g():
    """If user is logged in, add user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id


def create_wallet(user):
    """Create a wallet"""
    wallet = Wallets(user_id=user.id)
    db.session.add(wallet)
    db.session.commit()


def do_logout():
    """Loggout user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signing up.
     Create a new user and add it to the data base.
     Redirect to the home page.
     If form is not filled out properly, show form again. 
     If there is already a user with that username: flash message and show form again.   
     """
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data,
                               password=form.password.data,
                               email=form.email.data)
            db.session.commit()
            do_login(user)
            create_wallet(user)
            return redirect('/')

        except IntegrityError:
            flash('Username is already taken, please choose another one', 'danger')
            return render_template('users/signup.html', form=form)
    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login page.
    Show log in form.
    If form is filled out and authenticated, 
    then add user to session. 
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            email=form.email.data, password=form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')
        else:
            flash('Your user or password is not correct', 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user"""
    do_logout()
    # Give feedback to user
    flash('You have logged out', 'success')
    # Redirect to home page
    return redirect('/')


@app.route('/')
def homepage():
    """Show homepage:
    -anon users:
    -logged in user: Budget, Wallet, InvestingPeak
    """

    if g.user:
        wallet = g.user.wallet[0]
        wallet = g.user.wallet[0]
        total_spent = 0
        for trans in wallet.transactions:
            total_spent += trans.amt

        return render_template('home.html', user=g.user, wallet=wallet, total_spent=total_spent)
    else:
        return render_template('home-anon.html')


@app.route('/<int:user_id>/wallet', methods=['GET', 'POST'])
def wallet(user_id):
    """Show current amount in wallet.
    Show a form to add a new wallet.
    """
    user = User.query.get_or_404(user_id)

    if g.user == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = EditWallet()
    wallet = g.user.wallet[0]
    previos_amt = g.user.wallet[0].amt
    if form.validate_on_submit():
        try:
            wallet.amt = previos_amt + form.amt.data
            db.session.commit()
            flash(f'{form.amt.data} was added to your wallet.', 'success')
            return redirect(f'/{user_id}/wallet')
        except IntegrityError:
            flash('Please enter only numbers', 'danger')
            return render_template('users/wallet.html', form=form)

    return render_template('users/wallet.html', form=form, wallet=g.user.wallet)


@app.route('/<int:user_id>/budgets', methods=['GET', 'POST'])
def budgets(user_id):
    """Show current budgets.
    Show form to add a new budget"""

    if g.user == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    num_budgets = len(g.user.budgets)

    form = AddBudget()

    if form.validate_on_submit():
        new_budget = Budget(user_id=user_id, name=form.name.data)
        db.session.add(new_budget)
        db.session.commit()
        return redirect(f'/{g.user.id}/budgets')

    return render_template('budgets/budgets.html', form=form, budgets=g.user.budgets, num_budgets=num_budgets)


@app.route('/<int:user_id>/budgets/<int:budget_id>', methods=['GET', 'POST'])
def each_budget(user_id, budget_id):
    """ Show form to add categories to the budget.
    Show current categories of the budget.
    """
    if g.user == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    cur_budget = Budget.query.get_or_404(budget_id)
    num_cat = cur_budget.categories
    cur_budget.total_amt = 0
    for each_cat in num_cat:
        cur_budget.total_amt += each_cat.amt

    db.session.commit()

    form = AddCategory()

    if form.validate_on_submit():
        new_category = Category(budget_id=budget_id,
                                name=form.name.data, amt=form.amt.data)
        db.session.add(new_category)
        db.session.commit()
        return redirect(f'/{g.user.id}/budgets/{budget_id}')

    return render_template('budgets/eachbudget.html', form=form, cur_budget=cur_budget, num_cat=len(num_cat))


@app.route('/<int:user_id>/transactions', methods=['GET', 'POST'])
def transactions(user_id):
    """Seelect the budget to redirect to add transactions."""

    if g.user.id == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    wallet = g.user.wallet[0]
    total_spent = 0
    for trans in wallet.transactions:
        total_spent += trans.amt

    dynamic_choices = []
    for eachbudget in g.user.budgets:
        dynamic_choices.append((eachbudget.id, eachbudget.name))

    form = SelectBudget()
    form.budget_id.choices = dynamic_choices

    if form.validate_on_submit():
        budget_id = form.budget_id.data
        return redirect(f'/transactions/{g.user.id}/{budget_id}')

    return render_template("transactions/seetransactions.html", form=form, wallet=wallet, num_trans=len(wallet.transactions), total_spent=total_spent)


@app.route('/transactions/<int:user_id>/<int:budget_id>', methods=['GET', 'POST'])
def addtransaction(user_id, budget_id):
    """See previous transactions.
    Add a transaction."""

    if g.user.id == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    budget = Budget.query.get(budget_id)
    budget.total_amt = 0

    all_cat = budget.categories
    for each_cat in all_cat:
        budget.total_amt += each_cat.amt
    db.session.commit()

    # add new transaction
    dynamic_choices = []
    for eachcat in budget.categories:
        dynamic_choices.append((eachcat.id, eachcat.name))

    form = AddTransaction()
    form.cat_id.choices = dynamic_choices

    if form.validate_on_submit():
        cat_id = form.cat_id.data
        wallet_id = g.user.wallet[0].id
        amt = form.amt.data
        description = form.description.data
        transaction = Transactions(
            cat_id=cat_id, budget_id=budget.id, wallet_id=wallet_id, amt=amt, description=description)
        db.session.add(transaction)
        db.session.commit()
        return redirect(f'/transactions/{g.user.id}')

    return render_template('/transactions/addtransactions.html', form=form, budget=budget)
