import pytest
from flask import Flask
from list_products.list_products import app
import asyncio
import requests

base_url = "http://localhost:8001/"


def test_get_card():
    response = requests.get(f"{base_url}cart")
    print(response)
    assert response.status_code == 200


def test_post_card():
    response = requests.post(
        f"{base_url}cart", json={"id": 1, "name": "test", "price": 123}
    )
    assert response.status_code == 201
