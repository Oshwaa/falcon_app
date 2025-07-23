# Falcon REST API

A simple Falcon-based REST API built as part of my 1-week Junior Developer Training.

## 🚀 Project Overview

This project demonstrates a basic RESTful API using the [Falcon](https://falcon.readthedocs.io/en/stable/) web framework in Python. It supports basic CRUD-style operations and is structured for clarity and extendability.

## 📦 Features

- `GET /items` or `GET /items/json`: Retrieve all items in json
- `GET /items/csv`: Retrieve all items in CSV FORMAT
- `POST /items`: Add a new item (e.g. `{ "name": "Apple", "quantity": 5 }`)
- JSON request and response support
- Basic validation with Pydantic
- Modular and class-based route handlers

## 🛠️ Technologies Used

- Python 3.10+
- Falcon
- Pydantic
- Gunicorn (optional for production)
- Docker (for containerization)

## 🐳 Running with Docker

Build the Docker image:

```bash
docker build -t oshwa/falcon_app .
