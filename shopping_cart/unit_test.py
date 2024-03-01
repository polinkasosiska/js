import pytest
from flask_testing import TestCase
from shopping_cart import app, cart

class ShoppingCartTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

def test_get_cart_empty(self):
    response = self.client.get("/cart")
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_to_cart(self):
    item = {"id": 1, "name": "Necklace", "price": 100}
    response = self.client.post("/cart", json=item)
    assert response.status_code == 201
    assert response.get_json() == {"message": "Item added to cart"}
    assert cart == [item]

def test_clear_cart(self):
    cart.append({"id": 1, "name": "Necklace", "price": 100})
    response = self.client.delete("/cart")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Cart cleared"}
    assert cart == []

def test_remove_from_cart(self):
    cart.append({"id": 1, "name": "Necklace", "price": 100})
    response = self.client.delete("/cart/1")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Item removed from cart"}
    assert cart == []

def test_remove_non_existing_item(self):
    response = self.client.delete("/cart/1")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found in cart"}
