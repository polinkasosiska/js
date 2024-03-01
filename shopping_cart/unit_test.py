import pytest
from flask import Flask
from shopping_cart import app, cart

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_cart_empty(client):
    response = client.get('/cart')
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_to_cart(client):
    item = {"id": 1, "name": "Test Item"}
    response = client.post('/cart', json=item)
    assert response.status_code == 201
    assert response.get_json() == {"message": "Item added to cart"}
    assert cart == [item]

def test_clear_cart(client):
    item = {"id": 1, "name": "Test Item"}
    client.post('/cart', json=item)
    response = client.delete('/cart')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Cart cleared"}
    assert cart == []

def test_remove_from_cart(client):
    item = {"id": 1, "name": "Test Item"}
    client.post('/cart', json=item)
    response = client.delete('/cart/1')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Item removed from cart"}
    assert cart == []
