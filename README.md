# PostStack

A FastAPI-based RESTful API for managing posts and comments, with JWT authentication, PostgreSQL integration, and robust testing.

---

## Features

- **FastAPI**: High-performance Python web framework.
- **JWT Authentication**: Secure endpoints using JSON Web Tokens.
- **PostgreSQL**: Persistent storage for posts and comments.
- **Pydantic**: Data validation and settings management.
- **Testing**: Pytest-based test suite with async support.
- **CORS**: Configurable Cross-Origin Resource Sharing.
- **Logging**: Structured logging for debugging and monitoring.
- **Health Check**: `/health` endpoint for service monitoring.

---

## Project Structure

```
storeapi/
│
├── controller/
│   ├── controller.py
│   └── user.py
├── db/
│   ├── database.py
│   └── entity.py
├── security/
│   └── security.py
├── tests/
│   ├── conftest.py
│   └── routers/
│       └── test_post.py
├── main.py
├── logging_config.py
└── ...
```

---

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/storeapi.git
cd storeapi
```

### 2. Create a virtual environment and install dependencies

```sh
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/blog
SECRET_KEY=your_secret_key
ENV_STATE=DEV
```

### 4. Set up the PostgreSQL database

- Ensure PostgreSQL is running.
- Create the `blog` database:
  ```sh
  psql -U postgres
  CREATE DATABASE blog;
  ```

### 5. Run database migrations (if any)

*(Add Alembic or migration instructions here if used)*

---

## Running the Application

```sh
uvicorn storeapi.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## API Endpoints

- `GET /` — Welcome message
- `GET /health` — Health check
- `POST /posts/` — Create a new post (JWT required)
- `GET /posts/` — List all posts
- `DELETE /posts/{post_id}/comments/{comment_id}` — Delete a comment (JWT required)
- *(Add more endpoints as needed)*

---

## Testing

Run the test suite with:

```sh
pytest
```

- Uses `pytest`, `pytest-anyio`, and `httpx` for async endpoint testing.
- Fixtures in `conftest.py` provide test clients and database isolation.

---

## Troubleshooting

- **JWT Error: Signature has expired**  
  Obtain a new token or increase the expiration time in development.
- **psql not recognized**  
  Ensure PostgreSQL is installed and its `bin` directory is in your PATH.
- **Database does not exist**  
  Create the `blog` database in PostgreSQL.
- **Module import errors**  
  Avoid naming your files the same as libraries (e.g., `jwt.py`).

---

## License

MIT License

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [pytest](https://docs.pytest.org/)

---

*Feel free to customize this README to better fit your project’s specifics!*
