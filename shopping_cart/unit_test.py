import pytest
from flask import Flask
from shopping_cart import (
    app,
)  # интеграционный тест, тк он проверяет взаимодействие между различными частями приложения Flask, включая обработку HTTP-запросов и ответов.


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_card(client):
    response = client.get("/cart")
    assert response.status_code == 200


def test_post_card(client):
    response = client.post("/cart", json={"id": 1, "name": "test", "price": 123})
    assert response.status_code == 201
