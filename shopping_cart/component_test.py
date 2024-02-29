import pytest
from flask import Flask
import asyncio
import requests

# Базовый URL для тестирования
base_url = "http://localhost:8001/"

def test_get_card():
    # Тест для проверки GET-запроса к карте
    response = requests.get(f"{base_url}cart")
    # Отправка GET-запроса к конечной точке "cart"
    print(response)
    # Вывод ответа для отладки
    assert response.status_code == 200
    # Проверка, что статус ответа равен 200 (успешно), корректно обрабатывает GET-запросы.


def test_post_card():
    # Тест для проверки POST-запроса к карте
    response = requests.post(
        f"{base_url}cart", json={"id": 1, "name": "test", "price": 123}
    )
    # Отправка POST-запроса с данными карты
    assert response.status_code == 201
    # Проверка, что статус ответа равен 201 (создано), корректно обрабатывает POST-запросы для создания новых записей.
