# RAG Banking Assistant API

This project is a **Retrieval-Augmented Generation (RAG) banking assistant API** built using:

* Django
* Django REST Framework
* LangChain
* Google Gemini
* FAISS Vector Search
* PostgreSQL

It allows users to ask questions about banking information stored in a knowledge base.

---

## Features

* RAG-based question answering
* Document knowledge base
* FAISS vector search
* Google Gemini LLM integration
* REST API endpoint for queries
* Django admin for document management

---

## Tech Stack

* Python
* Django
* Django REST Framework
* LangChain
* FAISS
* PostgreSQL
* Google Gemini API

---

## Installation

Clone the repository:

git clone https://github.com/yourusername/rag-banking-assistant.git

cd rag-banking-assistant

Create a virtual environment:

python -m venv venv

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

---

## Environment Variables

Create a `.env` file in the root directory.

Example:

DJANGO_SECRET_KEY=your_secret_key

DEBUG=True

GOOGLE_API_KEY=your_google_api_key

DB_NAME=ragbank

DB_USER=raguser

DB_PASSWORD=password

DB_HOST=localhost

DB_PORT=5432

---

## Run Migrations

python manage.py migrate

---

## Run Server

python manage.py runserver

---

## API Endpoint

POST

/api/query/

Example request:

{
"query": "What is the minimum balance for a savings account?"
}

Response:

{
"answer": "The minimum balance required..."
}

---

## Admin Panel

Create a superuser:

python manage.py createsuperuser

Access:

http://127.0.0.1:8000/admin/

Upload knowledge base documents there.

---

## License

MIT License
