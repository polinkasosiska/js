from flask import Flask, jsonify, request
from flask_cors import CORS
from mysql.connector import connect, Error
import os
import time

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
    TracerProvider(resource=Resource.create({SERVICE_NAME: "list_products"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("list_products")

# Создаем Flask приложение
app = Flask(__name__)

CORS(app, origins=["*"])


# TODO Database
# Список ювелирных украшений
jewelry_items = [
    {"id": 1, "name": "Ring", "price": 100},
    {"id": 2, "name": "Necklace", "price": 200},
    {"id": 3, "name": "Earrings", "price": 50},
]


def start_con():
    with tracer.start_as_current_span("create_database_connection"):
        try:
            connection = connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", "root"),
            )
            print(connection)
            create_db_query = "CREATE DATABASE IF NOT EXISTS jewelry"
            use_db_query = "USE jewelry"
            create_table_query = (
                "CREATE TABLE IF NOT EXISTS jewelry (id int, name TEXT, price int)"
            )
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                cursor.execute(use_db_query)
                cursor.execute(create_table_query)
            connection.commit()
        except Error as e:
            print(e)
        return connection


# Эндпоинт для получения списка всех украшений
@app.route("/jewelry", methods=["GET"])
def get_jewelry():
    with tracer.start_as_current_span("get_jewelry"):
        data = []
        connection = start_con()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM jewelry.jewelry")

            for i in cursor.fetchall():
                data.append({"id": i[0], "name": i[1], "price": i[2]})
        return jsonify(data)


# Эндпоинт для добавления нового украшения
@app.route("/jewelry", methods=["POST"])
def add_jewelry():
    with tracer.start_as_current_span("add_jewelry"):
        data = request.get_json()
        connection = start_con()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO jewelry VALUES ({data['id']}, \"{data['name']}\", {data['price']});"
                )
                connection.commit()
        except Error as e:
            print(e)
        return {}


# Эндпоинт для главной страницы
@app.route("/")
def home():
    return """
	<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="style.css" />
  <title>Browser</title>
</head>

<body>
  <h1>
    Добро пожаловать в микросервис jstore
  </h1>
  <p>
    Приколочено гвоздями!!
    <img src="https://www.vprommetiz.ru/wp-content/uploads/2020/05/gvozdi-stroitelnye01.jpg" alt="Гвозди!" />
  </p>
</body>

</html> 
"""


# Запуск Flask приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
