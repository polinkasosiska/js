import pytest
from flask import Flask
from shopping_cart import (
    app,
) # Импортируем Flask-приложение из модуля shopping_cart

@pytest.fixture
def client():
    app.config["TESTING"] = True # Активируем режим тестирования в конфигурации Flask-приложения
    with app.test_client() as client: # Создаем тестовый клиент для отправки запросов к приложению
        yield client # Возвращаем тестовый клиент, чтобы он мог быть использован в тестах

def test_get_card(client): # Тест GET-запроса к конечной точке /cart
    response = client.get("/cart") # Отправляем GET-запрос к конечной точке /cart
    assert response.status_code == 200 # Проверяем, что статус ответа равен 200 (успешно)

def test_post_card(client): # Тест POST-запроса к конечной точке /cart
    response = client.post("/cart", json={"id": 1, "name": "test", "price": 123}) # Отправляем POST-запрос с данными карты
    assert response.status_code == 201 # Проверяем, что статус ответа равен 201 (создано)
