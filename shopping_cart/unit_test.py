import pytest
from flask import Flask
from shopping_cart import app, cart

# Фикстура для клиента тестирования Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Тест на получение пустой корзины
def test_get_cart_empty(client):
    # Отправляем GET запрос на эндпоинт /cart
    response = client.get('/cart')
    # Проверяем, что статус ответа равен 200 (OK)
    assert response.status_code == 200
    # Проверяем, что в ответе вернулся пустой список
    assert response.get_json() == []

# Тест на добавление товара в корзину
def test_add_to_cart(client):
    # Подготавливаем данные товара
    item = {"id": 1, "name": "Test Item"}
    # Отправляем POST запрос на эндпоинт /cart с данными товара
    response = client.post('/cart', json=item)
    # Проверяем, что статус ответа равен 201 (Created)
    assert response.status_code == 201
    # Проверяем, что в ответе вернулось сообщение об успешном добавлении
    assert response.get_json() == {"message": "Item added to cart"}
    # Проверяем, что товар был добавлен в корзину
    assert cart == [item]

# Тест на очистку корзины
def test_clear_cart(client):
    # Добавляем товар в корзину
    item = {"id": 1, "name": "Test Item"}
    client.post('/cart', json=item)
    # Отправляем DELETE запрос на эндпоинт /cart для очистки корзины
    response = client.delete('/cart')
    # Проверяем, что статус ответа равен 200 (OK)
    assert response.status_code == 200
    # Проверяем, что в ответе вернулось сообщение об успешной очистке
    assert response.get_json() == {"message": "Cart cleared"}
    # Проверяем, что корзина теперь пуста
    assert cart == []

# Тест на удаление товара из корзины
def test_remove_from_cart(client):
    # Добавляем товар в корзину
    item = {"id": 1, "name": "Test Item"}
    client.post('/cart', json=item)
    # Отправляем DELETE запрос на эндпоинт /cart/1 для удаления товара
    response = client.delete('/cart/1')
    # Проверяем, что статус ответа равен 200 (OK)
    assert response.status_code == 200
    # Проверяем, что в ответе вернулось сообщение об успешном удалении
    assert response.get_json() == {"message": "Item removed from cart"}
    # Проверяем, что корзина теперь пуста
    assert cart == []
