from flask import Flask, jsonify, request, session
from flask_cors import CORS

import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "shopping_cart"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("shopping_cart")

# Создаем Flask приложение
app = Flask(__name__)

CORS(app, origins=["*"])

# Список элементов в корзине
cart = []


# Эндпоинт для получения списка украшений в корзине
@app.route("/cart", methods=["GET"])
def get_cart():
    with tracer.start_as_current_span("get_cart"):
        return jsonify(cart)


# Эндпоинт для добавления украшения в корзину
@app.route("/cart", methods=["POST"])
def add_to_cart():
    with tracer.start_as_current_span("add_to_cart"):
        item = request.get_json()
        cart.append(item)
        return jsonify({"message": "Item added to cart"}), 201


# Эндпоинт для очистки корзины/\
@app.route("/cart", methods=["DELETE"])
def clear_cart():
    with tracer.start_as_current_span("clear_cart"):
        cart.clear()
        return jsonify({"message": "Cart cleared"}), 200


# Эндпоинт для удаления украшения из корзины
@app.route("/cart/<int:id>", methods=["DELETE"])
def remove_from_cart(id):
    with tracer.start_as_current_span("remove_from_cart"):
        for item in cart:
            if item["id"] == id:
                cart.remove(item)
                return jsonify({"message": "Item removed from cart"}), 200
        return jsonify({"error": "Item not found in cart"}), 404


# Запуск Flask приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 8001))
