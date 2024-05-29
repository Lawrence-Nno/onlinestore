from flask import Flask, request, redirect, render_template, url_for, flash, abort, session, jsonify
from flask_admin import Admin, BaseView
from flask_session import Session
import os.path as op
import requests
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from flask_migrate import Migrate
from database import Product, User, Cart, Order, db
from method_override import HTTPMethodOverrideMiddleware
from admin_view import ProductView, UserView, OrderView, MyAdminIndexView, RestrictedFileAdmin
from form import Form, SigninForm, SignUpForm, LoginForm, CartRemoveForm, PayForm, VerifyForm, ResetPasswordForm, ShippingAddressEditForm
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import os
from Country_States import countries_states


# Setting up the flask app
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

# Connecting the app to the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"

# Configuring the Flask Admin's interface
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# App's secret key to enable CSRF Protection
app.secret_key = os.getenv('SECRET_KEY', '')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', '')

# Enabling and initializing Flask's logging manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initializing the app with the database
db.init_app(app)
migrate = Migrate(app, db)

# Configuring the app with Mail settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', '')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('EMAIL', '')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD', '')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

year = datetime.now().strftime("%Y")


# Paystack Api Keys and urls for payment gateway
paystack_secret_key = os.getenv('PAYSTACK_SECRET', '')
paystack_public_key = os.getenv('PAYSTACK_PUBLIC', '')
url = os.getenv('PAYSTACK_URL', '')
headers = {
    "Authorization": f"Bearer {paystack_secret_key}",
    "Content-Type": "application/json",
}


# Adding the Admin Model Views for the admin site
admin = Admin(app, name='MyAdmin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(ProductView(Product, db.session))
admin.add_view(OrderView(Order, db.session))
admin.add_view(UserView(User, db.session))
path = op.join(op.dirname(__file__), 'static/hair_images')
admin.add_view(RestrictedFileAdmin(path, '/static', name='Hair Images'))


def admin_decorator(func):
    """
    Admin decorator, to ensure only the admin gets access to the view/function with this decorator
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if current_user.email != 'lawrence.nno@gmail.com' or not current_user.is_authenticated:
            return abort(403)
        else:
            return func(*args, **kwargs)
    # wrapper_func.__name__ = func.__name__
    return wrapper_func


def check_confirmed(func):
    """
    The decorator to check if a user's email has been confirmed
    :param func:
    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def user_loader(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


def generate_confirmation_token(email):
    """
    Generates the url for email confirmation
    :param email:
    :return: The url
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=10800):
    """
    Confirms the email confirmation url before the time runs out.
    :param token:
    :param expiration:
    :return:
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_mail(to, subject, html_msg):
    """
    This func sends out the email confirmation link
    :param to:
    :param subject:
    :param html_msg:
    :return:
    """
    msg = Message(subject, sender="classiccream@yahoo.com", recipients=[to])
    msg.body = html_msg
    mail.send(msg)
    print("Message sent")


@app.before_request
def track_history():
    # Skip if the request is AJAX or the request method is not GET
    if request.endpoint == 'static' or request.method != 'GET':
        return
    # Get the current history list from session
    history = session.get('history', [])
    # Add the current URL to the history list
    history.append(request.url)
    # Keep only the last three URLs
    if len(history) > 3:
        history.pop(0)
    # Save the updated history back to the session
    session['history'] = history


@app.route("/", methods=["GET", "POST"])
def index():
    """
    The home page function
    :return:
    """
    form = Form()
    products = db.session.execute(db.select(Product).order_by(Product.id)).scalars()
    return render_template('index.html', products=products, form=form, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route("/detail/<int:idx>", methods=["GET", "POST"])
def detail(idx):
    """
    The details page function
    :param idx:
    :return:
    """
    form = Form()
    product = db.session.execute(db.select(Product).where(Product.id == idx)).scalar()
    if product:
        static_folder = os.path.join(app.root_path, 'static')
        image_folder = os.path.join(app.root_path, 'static/hair_images')
        video_folder = os.path.join(app.root_path, 'static/videos')
        image_f = product.image.split('.')
        image_format = image_f[0][12:-1]
        image_files = []
        for root, dirs, files in os.walk(image_folder):
            for file in files:
                if file.startswith(image_format):
                    # Add the relative path of the image to the list
                    rel_path = os.path.relpath(os.path.join(root, file), static_folder)
                    rel_path = rel_path.replace("\\", "/")
                    image_files.append(rel_path)
                    print(image_files)
        no_of_images = len(image_files)
        images = [(num + 1, item) for num, item in enumerate(image_files)]

        video_files = []
        for root, dirs, files in os.walk(video_folder):
            for file in files:
                if file.startswith(image_format):
                # if image_format in file:
                    rel_path = os.path.relpath(os.path.join(root, file), static_folder)
                    rel_path = rel_path.replace("\\", "/")
                    video_files.append(rel_path)
                    print(video_files)
        if len(video_files) > 0:
            videos = [(num + 1, item) for num, item in enumerate(video_files)]
        else:
            videos = None

        if request.method == "POST":
            if current_user.is_authenticated:
                item = db.session.execute(db.select(Cart).where(Cart.product_id == idx)).scalar()
                if item:
                    method = "PATCH"
                    if method in ["GET", "POST", "PATCH"]:
                        item.quantity += 1
                        item.subtotal = item.quantity * product.price
                        db.session.commit()
                else:
                    item = Cart(
                        quantity=1,
                        subtotal=product.price,
                        product_id=idx,
                        user_id=current_user.id
                    )
                    db.session.add(item)
                    db.session.commit()
            else:
                return redirect(url_for('signin'))
            return redirect(url_for('detail', idx=idx))
        return render_template('detail.html', product=product, logged_in=current_user.is_authenticated, user=current_user, form=form, year=year, images=images, videos=videos, no_of_images=no_of_images)
    else:
        abort(404)


@app.route("/cart/<int:idx>", methods=["GET", "POST", "PATCH"])
def cart(idx):
    """
    This function handles adding products to cart
    :param idx:
    :return:
    """
    # idx = request.args.get("productId", "")
    if request.method == "POST":
        product = db.session.execute(db.select(Product).where(Product.id == idx)).scalar()
        item = db.session.execute(db.select(Cart).where(Cart.product_id == idx)).scalar()
        if item:
            method = "PATCH"
            if method in ["GET", "POST", "PATCH"]:
                item.quantity += 1
                item.subtotal = item.quantity * product.price
                db.session.commit()
        else:
            if current_user.is_authenticated:
                item = Cart(
                    quantity=1,
                    subtotal=product.price,
                    product_id=idx,
                    user_id=current_user.id
                )
                db.session.add(item)
                db.session.commit()
            else:
                return redirect(url_for('signin'))

        return redirect(url_for('index') + f"#{idx}")


@app.route("/all_cart", methods=["GET", "POST"])
def all_cart():
    """
    This functions displays the cart page and also handles the total sum.
    :return:
    """
    if current_user.is_authenticated:
        form_inc = CartRemoveForm()
        form_inc.submit.label.text = '+'

        form_dec = CartRemoveForm()
        form_dec.submit.label.text = '-'

        form = CartRemoveForm()
        # products = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.id)).scalars()
        items = Cart.query.where(Cart.user_id == current_user.id)
        indexed_items = [(num + 1, item) for num, item in enumerate(items)]
        subtotal = 0
        for num, entry in indexed_items:
            subtotal += entry.subtotal
        if subtotal > 0:
            shipping_price = 3500
        else:
            shipping_price = 0
        total = subtotal + shipping_price
        if request.method == "POST":
            btn = request.args.get('btn', '')
            if btn == '+':
                idx = request.args.get("id", "")
                if idx:
                    item = Cart.query.where(Cart.id == idx).scalar()
                    item.quantity += 1
                    item.subtotal = item.quantity * item.product.price
                    db.session.commit()
                return redirect(url_for('all_cart') + f"#{idx}")

            btn = request.args.get('btn', '')
            if btn == '-':
                idx = request.args.get("id", "")
                if idx:
                    item = Cart.query.where(Cart.id == idx).scalar()
                    if item.quantity > 1:
                        item.quantity -= 1
                        item.subtotal = item.quantity * item.product.price
                        db.session.commit()
                return redirect(url_for('all_cart') + f"#{idx}")

            idx = request.args.get("id", "")
            if idx:
                item = Cart.query.where(Cart.id == idx).scalar()
                db.session.delete(item)
                db.session.commit()
            return redirect(url_for('all_cart') + f"#{idx}")
    else:
        return redirect(url_for('signin'))
    return render_template('cart.html', products=indexed_items, subtotal=subtotal, shipping_price=shipping_price, total=total, form=form, form_inc=form_inc, form_dec=form_dec, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route('/order', methods=["GET", "POST"])
def order():
    """
    Once a cart list has been paid, this page converts the ordered items to an order page. This is the page that tells
    the customer of the order status.
    :return:
    """
    orders = Order.query.where(Order.user_id == current_user.id)
    indexed_orders = [(num + 1, item) for num, item in enumerate(orders)]
    return render_template('order.html', orders=indexed_orders, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """
    This page communicates with the Paystack API and handles the payment
    :return:
    """
    total = request.args.get('total', 0)
    form = PayForm()
    if request.method == "POST":
        data = {
            "amount": total,  # 500000
            "email": current_user.email,  # "customer@example.com"
            "callback_url": url_for('verify', _external=True),
        }
        response = requests.post(url, headers=headers, json=data)

        # Check the response status code and data
        if response.status_code == 200:
            print("Transaction initialized successfully.")
            # You can access the JSON response data
            data = response.json()
            print("Response data:", data)
            print(data['data']['reference'])
            print(data['data']['authorization_url'])
        else:
            print(f"Failed to initialize transaction. Status code: {response.status_code}.")
            # If there's an error message, print it
            if response.text:
                print("Error:", response.text)
                flash("Couldn't initialize transaction, please try again", category="error")
                return redirect(url_for('all_cart'))
        return_url = url_for('verify', code=data['data']['reference'], _external=True)
        checkout_url = data['data']['authorization_url']
        return redirect(checkout_url)
    return render_template('checkout.html', form=form, logged_in=current_user.is_authenticated, user=current_user, year=year, total=total)


@app.route('/verify', methods=["GET", "POST"])
def verify():
    """
    This page handles the payment verification
    :return:
    """
    form = VerifyForm()
    trxref = request.args.get('trxref', '')
    reference = request.args.get('reference', '')
    if request.method == "POST":
        # Headers for the HTTP request
        headers = {
            "Authorization": f"Bearer {paystack_secret_key}",
        }

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("Transaction verified successfully.")
            verification_data = response.json()
            print("Response data:", verification_data)
            orders = db.session.execute(db.select(Cart).where(Cart.user_id == current_user.id)).scalars()
            for item in orders:
                order = Order(
                    quantity=item.quantity,
                    subtotal=item.subtotal,
                    product_id=item.product_id,
                    user_id=item.user_id,
                    status="Paid | Awaiting Delivery",
                    reference=trxref,
                )
                db.session.add(order)
                db.session.commit()
                db.session.delete(item)
                db.session.commit()
        else:
            print(f"Failed to verify transaction. Status code: {response.status_code}.")
            print("Error message:", response.text)
        return redirect(url_for('index'))
    return render_template('verify.html', form=form, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    This func handles the signup
    :return:
    """
    form = SignUpForm()
    email = request.args.get('email', '')
    if email:
        form.email.data = email
    # form.country.choices = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua & Deps', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Rep', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo (Democratic Rep)', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland (Republic)', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea North', 'Korea South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 'St Kitts & Nevis', 'St Lucia', 'Saint Vincent & the Grenadines', 'Samoa', 'San Marino', 'Sao Tome & Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
    # form.state.choices = ['Abuja (FCT)', 'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara']
    if form.validate_on_submit():
        if form.password.data != form.confirm.data:
            flash("Password doesn't match")
            return render_template('signup', form=form)

        password = generate_password_hash(form.password.data, method='scrypt', salt_length=16)
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            phone=form.phone.data,
            email=form.email.data.lower(),
            password=password,
            country =form.country.data,
            state=form.state.data,
            localgovt=form.localgovt.data,
            city=form.city.data,
            address=form.address.data,
            registered_on=datetime.now(),
            confirmed=False,
            confirmed_on=None,
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html_msg = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_mail(user.email, subject, html_msg)

        login_user(user)

        flash("A confirmation email has been sent via email", "success")
        return redirect(url_for('unconfirmed'))
    return render_template('signup.html', form=form, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route('/get_states/<country>')
def get_states(country):
    states = countries_states.get(country, [])
    return jsonify(states)


@app.route('/profile/<idx>', methods=["GET"])
@login_required
def profile(idx):
    return render_template('profile.html', logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route('/address/<idx>', methods=["GET", "POST", "PATCH"])
@login_required
def edit_address(idx):
    form = ShippingAddressEditForm()
    user = db.session.execute(db.select(User).where(User.id == idx)).scalar()
    form.localgovt.data = user.localgovt
    form.city.data = user.city
    form.address.data = user.address
    if form.validate_on_submit():
        form = ShippingAddressEditForm()
        user.country = form.country.data
        user.state = form.state.data
        user.localgovt = form.localgovt.data
        user.city = form.city.data
        user.address = form.address.data
        db.session.commit()
        flash("Shipping Address is successfully Edited", "success")

        # Get the history from the session
        history = session.get('history', [])
        # Determine the two-step-back URL
        two_steps_back = history[-3] if len(history) >= 3 else url_for('index')

        return redirect(two_steps_back)
        # return redirect(url_for('profile', idx=current_user.id))
    return render_template('address_edit.html', form=form, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route('/confirm/<token>', methods=["GET", "POST", "PATCH"])
@login_required
def confirm_email(token):
    """
    This func handles the email confirmation
    :param token:
    :return:
    """
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation is invalid or has expired.", "danger")
        return redirect(url_for('unconfirmed'))

    if email:
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash("Account already confirmed", "success")
            return redirect(url_for('index'))
        else:
            user.confirmed = True
            user.confirmed_on = datetime.now()
            # db.session.add(user)
            db.session.commit()
            flash("Your account has now been confirmed. Happy Shopping!", "success")
            return redirect(url_for('index'))
    else:
        flash("The confirmation is invalid or has expired.", "danger")
        return redirect(url_for('unconfirmed'))
    # return redirect(url_for('index'))


@app.route('/unconfirmed', methods=["GET", "POST"])
@login_required
def unconfirmed():
    """
    Displays the page for users to go to when not confirmed
    :return:
    """
    return render_template('unconfirmed.html', user=current_user, logged_in=current_user.is_authenticated, year=year)


@app.route('/resend')
@login_required
def resend_confirmation():
    """
    Handles the email confirmation resend link
    :return:
    """
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html_msg = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_mail(current_user.email, subject, html_msg)
    flash("A new confirmation has been sent", "success")
    return redirect(url_for('unconfirmed'))


@app.route('/password_reset_link')
def password_reset_link():
    user_email = request.args.get('email', '')
    token = generate_confirmation_token(user_email)
    reset_password_url = url_for('reset_password', token=token, _external=True)
    html_msg = render_template('password_reset.html', reset_password_url=reset_password_url)
    subject = "Please reset your password"
    send_mail(user_email, subject, html_msg)
    flash("A password reset link has been sent to your email", "success")
    return redirect(url_for('login'))


@app.route('/reset_password/<token>', methods=["GET", "POST", "PATCH"])
def reset_password(token):
    """
    This func handles password reset function
    :param token:
    :return:
    """
    form = ResetPasswordForm()
    try:
        email = confirm_token(token)
    except:
        flash("The password reset link is invalid or has expired", "danger")
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first_or_404()
    form.email.data = email
    if email:
        if form.validate_on_submit():
            if form.password.data != form.confirm.data:
                flash("Password Mismatch", "error")
                return redirect(url_for('reset_password', token=token))

            # user = User.query.filter_by(email=email).first_or_404()
            password = generate_password_hash(form.password.data, method='scrypt', salt_length=16)
            user.password = password
            db.session.commit()
            flash("Password Reset was successful, please login. Happy Shopping!", "success")
            return redirect(url_for('login'))
    else:
        flash("The password reset link is invalid or has expired.", "danger")
    return render_template('reset_password.html', form=form, user=user, year=year)


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Handles the login page and redirects to unconfirmed users if the user isn't confirmed yet
    :return:
    """
    form = LoginForm()
    reset = request.args.get('reset', '')
    email = request.args.get('email', '')
    if email:
        form.email.data = email

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data.lower())).scalar()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.confirmed:
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('unconfirmed'))
            else:
                flash("Incorrect password", "error")
                return redirect(url_for('login', reset=True, email=form.email.data))
        else:
            flash("User not found, Sign up instead", category="error")
            return redirect(url_for('signup'))
    return render_template('login.html', form=form, logged_in=current_user.is_authenticated, user=current_user, reset=reset, year=year)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    """
    Handles logout
    :return:
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/signin', methods=["GET", "POST"])
def signin():
    """
    This func handles users that wants to add products to their cart without logging in.
    It redirects them to the signup page or login page depending if they have initially registered.
    :return:
    """
    form = SigninForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data.lower())).scalar()
        if user:
            return redirect(url_for('login', email=form.email.data))
        else:
            return redirect(url_for('signup', email=form.email.data))
    return render_template('signin.html', form=form, logged_in=current_user.is_authenticated, user=current_user, year=year)


@app.route('/filter/<hairstyle>')
def filter_hair(hairstyle):
    """
    This function filters the database and returns the selected kind of hair
    :param hairstyle:
    :return:
    """
    form = Form()
    products = db.session.execute(db.select(Product).where(Product.name.ilike(f"%{hairstyle}%"))).scalars().all()
    return render_template('index.html', products=products, form=form, logged_in=current_user.is_authenticated,
                           user=current_user, year=year)


@app.route('/admin/')
@login_required
@admin_decorator
def admin_panel():
    return render_template('admin/admin_base.html', title='Admin Dashboard')


if __name__ == "__main__":
    app.run(host="0.0.0.0")

# with app.app_context():
#     # metadata = MetaData()
#     # table = Table('User', metadata, autoload_with=db.engine)
#     # table.drop(bind=db.engine)
#     db.create_all()