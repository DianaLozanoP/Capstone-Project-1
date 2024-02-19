from flask import Flask, render_template, request, redirect, session, flash, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os
import requests
from models import connect_db, db, User, Budget, Category, Transactions, Wallets, MutualFunds, ETFs
from forms import UserAddForm, LoginForm, AddBudget, AddCategory, EditWallet, SelectBudget, AddTransaction, FilterETF, filterMutualFunds
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError
from seed import seedETFs, seedMTs
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from sqlalchemy import func

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)
csrf = CSRFProtect(app)

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


def create_wallet(user_id):
    """Create a wallet"""
    wallet = Wallets(user_id=user_id)
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
    print("Not validated form", form.username.data)
    if form.validate_on_submit():
        print("It was validated", form.username.data)
        try:
            user = User.signup(username=form.username.data,
                               password=form.password.data,
                               email=form.email.data)
            db.session.commit()
            do_login(user)
            create_wallet(user.id)
            return redirect('/')
        except IntegrityError:
            flash('Username is already taken, please choose another one', 'danger')
            return render_template('users/signup.html', form=form)
       
    else:
            # Display validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')
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
            flash('Your email or password is not correct', 'danger')

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
        num_budgets = len(g.user.budgets)
        wallet = g.user.wallet[0]
        wallet = g.user.wallet[0]
        total_spent = 0
        for trans in wallet.transactions:
            total_spent += trans.amt
        return render_template('home.html', num_budgets=num_budgets, user=g.user, wallet=wallet, total_spent=total_spent)
    else:
        return render_template('home-anon.html')


@app.route('/user/<int:user_id>')
def user_page(user_id):
    """Show basic info about user"""

    if g.user == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    return render_template('/users/profile.html')


@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit the user page"""
    if g.user == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserAddForm()
    if form.validate_on_submit():
        if User.authenticate(g.user.email,
                             form.password.data):
            g.user.username = form.username.data
            g.user.email = form.email.data
            db.session.commit()
            flash('Your user has been updated', 'success')
            return redirect(f'/user/{g.user.id}')
    # Pre-fill the form with current information
    # Allow user to edit the form
    form.username.data = g.user.username
    form.email.data = g.user.email
    return render_template('/users/profile_edit.html', form=form)


@app.route('/wallet/<int:user_id>', methods=['GET', 'POST'])
def wallet(user_id):
    """Show current amount in wallet.
    Show a form to add money into the wallet.
    """

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
            return redirect(f'/wallet/{user_id}')
        except IntegrityError:
            flash('Please enter only numbers', 'danger')
            return render_template('users/wallet.html', form=form)

    return render_template('users/wallet.html', form=form, wallet=g.user.wallet)


@app.route('/budgets/<int:user_id>', methods=['GET', 'POST'])
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
        return redirect(f'/budgets/{g.user.id}')

    return render_template('budgets/budgets.html', form=form, budgets=g.user.budgets, num_budgets=num_budgets)


@app.route('/budgets/<int:user_id>/<int:budget_id>', methods=['GET', 'POST'])
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
        return redirect(f'/budgets/{g.user.id}/{budget_id}')

    return render_template('budgets/eachbudget.html', form=form, cur_budget=cur_budget, num_cat=len(num_cat))


@app.route('/budgets/<int:user_id>/<int:budget_id>/delete', methods=['GET'])
def delete_budget(user_id, budget_id):
    """Delete the budget and its transactions"""
    if g.user == None or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    cur_budget = Budget.query.get_or_404(budget_id)
    db.session.delete(cur_budget)
    db.session.commit()
    return redirect(f'/budgets/{g.user.id}')


@app.route('/transactions/<int:user_id>/', methods=['GET', 'POST'])
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
        g.user.wallet[0].amt = g.user.wallet[0].amt - form.amt.data
        amt = form.amt.data
        description = form.description.data
        category = Category.query.get(cat_id)
        category.amt_spent = category.amt_spent + form.amt.data
        transaction = Transactions(
            cat_id=cat_id, budget_id=budget.id, wallet_id=wallet_id, amt=amt, description=description)
        db.session.add(transaction)
        db.session.commit()
        return redirect(f'/transactions/{g.user.id}')

    return render_template('/transactions/addtransactions.html', form=form, budget=budget)

# request to external API:


@app.route('/get-etfs', methods=['GET'])
def get_data():
    # api_key = 'B9Z5vi037YMNUP4lElt7iH1HQskbVYUm'
    # api_url = f'https://financialmodelingprep.com/api/v3/etf/list?apikey={api_key}'
    api_url = 'https://api.twelvedata.com/etf'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            answer = seedETFs(data)
            return answer
        else:
            return jsonify({'error': 'Failed to fetch data from the API'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-mutualfunds', methods=['GET'])
def get_mf():

    api_key = '2592458fd15047328e6683d9ac51e10d'
    api_url = f'https://api.twelvedata.com/mutual_funds/list?fund_family=Vanguard&apikey={api_key}'

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            answer = seedMTs(data)
            return answer
        else:
            return jsonify({'error': 'Failed to fetch data from the API'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/IndexFunds', methods=["GET", "POST"])
def show_indexfunds():
    """Explain about Index Funds.
    Introduce ETFs.
    Introduce Mutual Funds"""

    return render_template('/indexfunds/intro.html')


@app.route('/IndexFunds/ETFs', methods=['GET', 'POST'])
def etfs_page():
    """Show the list of all ETFs obtain from API"""
    list_query = ETFs.query.all()
    country_counts = db.session.query(
        ETFs.country, db.func.count().label('count')).group_by(ETFs.country)
    dynamic_choices = []
    for country in country_counts:
        dynamic_choices.append((country[0], country[0]))
    form = FilterETF()
    form.country.choices = sorted(dynamic_choices)

    if form.validate_on_submit():
        country = form.country.data
        return redirect(f'/IndexFunds/ETFs/filter?country={country}')

    return render_template('/indexfunds/etfs.html', form=form, dynamic_choices=dynamic_choices, list_query=list_query)


@app.route('/IndexFunds/ETFs/filter')
def country_list():
    """Show a lit of filtered ETFs by country"""
    country = request.args.get('country')
    filter_query = ETFs.query.filter_by(country=f'{country}')
    return render_template('/indexfunds/list_etf_filter.html', list_query=filter_query, country=country)


@app.route('/IndexFunds/MutualFunds', methods=["GET", "POST"])
def get_mutualfunds():
    """Show a list of all Mutual Funds"""
    list_query = MutualFunds.query.all()

    ratings = db.session.query(
        MutualFunds.performance_rating, db.func.count().label('performance_rating')).group_by(MutualFunds.performance_rating)
    dynamic_choices = []
    for num in ratings:
        dynamic_choices.append((num[0], num[0]))
    form = filterMutualFunds()
    form.performance_rating.choices = sorted(dynamic_choices)

    if form.validate_on_submit():
        performance_rating = form.performance_rating.data
        return redirect(f'/IndexFunds/MutualFunds/filter?performance={performance_rating}')

    return render_template('indexfunds/mutualfunds.html', list_query=list_query, form=form,  dynamic_choices=dynamic_choices)


@app.route('/IndexFunds/MutualFunds/filter')
def country_list_mutual():
    """Show a lit of filtered Mutual Funds by performance rating"""
    performance = request.args.get('performance')
    filter_query = MutualFunds.query.filter_by(
        performance_rating=f'{performance}')
    return render_template('/indexfunds/list_filter.html', list=filter_query, performance=performance)


@app.route('/get-transactions')
def send_transactions():
    """Send data to JS to create the pie table"""
    wallet = g.user.wallet[0]
    filter_by_month = db.session.query(Transactions).filter(
        func.extract('month', Transactions.timestamp) == datetime.now().month,
        func.extract('year', Transactions.timestamp) == datetime.now().year,
        Transactions.wallet_id == wallet.id).all()
    data = {}
    for each in filter_by_month:  
        data[each.category.name]= each.amt
    return jsonify({"data": data})
