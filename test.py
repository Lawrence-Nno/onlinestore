from datetime import datetime

import pytest
from flask import url_for
from onlinestore import app, db, check_password_hash, generate_password_hash, generate_confirmation_token
from onlinestore import User, Product, Cart, Order
from flask_login import login_user, current_user
from onlinestore import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        # with app.app_context():
            # db.create_all()
        yield client
        # db.drop_all()


@pytest.fixture
def init_database():
    with app.app_context():
        user = User(
            email='test@example.com',
            password=generate_password_hash('password'),
            firstname='first',
            lastname='last',
            phone='090880900',
            country='testland',
            state='teststate',
            localgovt='testgovt',
            city='testcity',
            address='testdress',
            registered_on=datetime.now(),
            confirmed=False,
            confirmed_on=None,
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        user = db.session.execute(db.select(User).where(User.firstname == 'first')).scalar()
        return user


def test_index(client):
    with client.application.app_context():
        response = client.get(url_for('index'))
        assert response.status_code == 200
        assert b"I'm shopping for ..." in response.data


def test_detail(client):
    with client.application.app_context():
        product = Product(name='Test Product', price=100, desc='A good test hair', image='hair_images/aihair.jpg')
        db.session.add(product)
        db.session.commit()
        response = client.get(url_for('detail', idx=product.id))
        assert response.status_code == 200
        assert b'Test Product' in response.data


# def test_cart(client, init_database):
#     with client.application.app_context():
#         product = Product(name='Test Product1', price=100, desc='A good test hair', image='hair_images/aihair.jpeg')
#         db.session.add(product)
#         db.session.commit()
#         client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'})
#         response = client.post(url_for('cart', idx=product.id))
#         assert response.status_code == 302  # Redirect to cart page
#         # cart_item = Cart.query.filter_by(user_id=init_database.id, product_id=product.id).first()
#         cart_item = db.session.execute(db.select(Cart).where(Cart.product_id == product.id)).scalar()
#         assert cart_item is not None
#         assert cart_item.quantity == 1
def test_cart(client, init_database):
    with client.application.app_context():
        # Create and add product to database
        product = Product(name='Test Product1', price=100, desc='A good test hair', image='hair_images/aihair.jpeg')
        db.session.add(product)
        db.session.commit()

        # Log in the user
        login_response = client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        assert login_response.status_code == 200, "Login passed"
        assert current_user.is_authenticated

        # Add product to cart
        add_to_cart_response = client.post(url_for('cart', idx=product.id))
        assert add_to_cart_response.status_code == 302, "Product added to cart"

        # Verify product in cart
        cart_item = db.session.execute(db.select(Cart).where(Cart.user_id == init_database.id, Cart.product_id == product.id)).scalar()
        print("Cart Item:", cart_item)
        print("Product:", product)
        assert cart_item is not None, "Product was added to cart"
        assert cart_item.quantity == 1


def test_signup(client):
    with client.application.app_context():
        response = client.post(url_for('signup'), data={
            'firstname': 'John',
            'lastname': 'Doe',
            'phone': '0920880900',
            'email': 'dc8830135@gmail.com',
            'password': 'password',
            'confirm': 'password',
            'country': 'Nigeria',
            'state': 'Imo',
            'localgovt': 'testgovt',
            'city': 'testcity',
            'address': 'testdress'
        }, follow_redirects=True)
        assert response.status_code == 200  # Redirect to unconfirmed page
        assert current_user.is_authenticated
        user = db.session.execute(db.select(User).where(User.email == 'dc8830135@gmail.com')).scalar()
        assert user is not None
        assert user.firstname == 'John'


def test_login(client):
    with client.application.app_context():
        response = client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'})
        assert response.status_code == 302  # Redirect to index
        assert current_user.is_authenticated


def test_logout(client):
    with client.application.app_context():
        client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'})
        response = client.get(url_for('logout'))
        assert response.status_code == 302  # Redirect to index
        assert not current_user.is_authenticated


def test_order(client):
    with client.application.app_context():
        client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'})
        response = client.get(url_for('order'))
        assert response.status_code == 200
        assert b'Status' in response.data


def test_checkout(client):
    with client.application.app_context():
        client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'})
        response = client.post(url_for('checkout'), data={'total': 1000})
        assert response.status_code == 302  # Redirect to payment page


def test_verify(client):
    with client.application.app_context():
        client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'password'})
        response = client.get(url_for('verify', trxref='dummy', reference='dummy'))
        assert response.status_code == 200
        assert b'verify' in response.data


def test_resend_confirmation(client):
    with client.application.app_context():
        client.post(url_for('login'), data={'email': 'classicgab@gmail.com', 'password': '12345'})
        response = client.get(url_for('resend_confirmation'))
        assert response.status_code == 302  # Redirect to unconfirmed page


def test_reset_password(client):
    with client.application.app_context():
        token = generate_confirmation_token('test@example.com')
        response = client.post(url_for('reset_password', token=token), data={
            'email': 'test@example.com',
            'password': 'newpassword',
            'confirm': 'newpassword'
        })
        assert response.status_code == 302  # Redirect to login page
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert check_password_hash(user.password, 'newpassword')


def test_admin_access(client):
    with client.application.app_context():
        admin_user = User(
            email='admin@example.com',
            password=generate_password_hash('admin'),
            is_admin=True,
            firstname='Admin',
            lastname='Last',
            phone='090880900',
            country='testland',
            state='teststate',
            localgovt='testgovt',
            city='testcity',
            address='testdress',
            registered_on=datetime.now(),
            confirmed=True,
            confirmed_on=datetime.now()
        )
        db.session.add(admin_user)
        db.session.commit()
        client.post(url_for('login'), data={'email': 'admin@example.com', 'password': 'admin'})
        response = client.get(url_for('admin.index'))
        assert response.status_code == 200
        assert b'Back to Home' in response.data


def test_unconfirmed(client):
    with client.application.app_context():
        response = client.post(url_for('login'), data={'email': 'test@example.com', 'password': 'newpassword'})
        assert response.status_code == 302  # redirects to the unconfirmed page

        response2 = client.get(url_for('unconfirmed'))
        assert response2.status_code == 200  # redirects to the index page
        assert b'You have not confirmed your account' in response2.data
