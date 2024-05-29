import pytest
from onlinestore import app, User, Product, Cart, Order, db
from onlinestore import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"I'm shopping for ..." in response.data  # Assuming this text is in the index.html template


def test_index_post(client):
    response = client.post('/')
    assert response.status_code == 200
    assert response.request.path == "/"
    # Add assertions for post request behavior as needed


# def test_index_logged_in(client, logged_in_user):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b"Hi " in response.data
#     # Add assertions for behavior when user is logged in


def test_detail_get(client):
    response = client.get('/detail/1')
    assert response.status_code == 200
    assert b'Bone Straight' in response.data  # Assuming this text is in the detail.html template


def test_detail_invalid_product_id(client):
    response = client.get('/detail/999')
    assert response.status_code == 404
    assert b'Not Found' in response.data  # Assuming this text is in the detail.html template or a custom error page


def test_detail_post_allowed(client):
    response = client.post('/detail/2')
    assert response.status_code == 302
    # assert b'Method Not Allowed' in response.data  # Assuming this is the default Flask message for method not allowed


# def test_detail_logged_in(client, logged_in_user):
#     response = client.get('/detail/1')
#     assert response.status_code == 200
#     # Add assertions for behavior when user is logged in


def test_detail_not_logged_in(client):
    response = client.get('/detail/1')
    assert response.status_code == 200
    # Add assertions for behavior when user is not logged in


def test_index_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Account" in response.data
    # Add assertions for behavior when user is not logged in