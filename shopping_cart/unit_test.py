import pytest
from flask_testing import TestCase
from shopping_cart import app # имя моего приложения

class TestCartAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_cart_empty(self):
        response = self.client.get('/cart')
        assert response.status_code == 200
        assert response.json == []

    def test_add_to_cart(self):
        item = {"id": 1, "name": "Test Item"}
        response = self.client.post('/cart', json=item)
        assert response.status_code == 201
        assert response.json == {"message": "Item added to cart"}

        # Проверяем, что элемент действительно добавлен
        response = self.client.get('/cart')
        assert response.json == [item]

    def test_clear_cart(self):
        item = {"id": 1, "name": "Test Item"}
        self.client.post('/cart', json=item)
        response = self.client.delete('/cart')
        assert response.status_code == 200
        assert response.json == {"message": "Cart cleared"}

        # Проверяем, что корзина очищена
        response = self.client.get('/cart')
        assert response.json == []

    def test_remove_from_cart(self):
        item = {"id": 1, "name": "Test Item"}
        self.client.post('/cart', json=item)
        response = self.client.delete('/cart/1')
        assert response.status_code == 200
        assert response.json == {"message": "Item removed from cart"}

        # Проверяем, что элемент действительно удален
        response = self.client.get('/cart')
        assert response.json == []

    def test_remove_from_cart_not_found(self):
        response = self.client.delete('/cart/1')
        assert response.status_code == 404
        assert response.json == {"error": "Item not found in cart"}
