# 🎉 Fest-API

A scalable and high-performance REST API built with **FastAPI**, designed to manage and retrieve information
effortlessly for all fests hosted by **MIT Bengaluru**—whether they are cultural, technical, or anything in between.

---

<!--suppress HtmlDeprecatedAttribute -->
<p align="center">
  <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI Logo" width="150"/>
</p>


A scalable and high-performance fest API built with **FastAPI**, designed to manage and retrieve information
effortlessly for all fests in MIT Bengaluru; whether they be cultural, technical or anything in between.

---

## 📚 Table of Contents

- [✨ Features](#-features)
- [⚙️ Installation](#-installation)
- [🚀 Getting Started with the API](#-getting-started-with-the-api)
- [📜 Documentation and OpenAPI Specification](#-documentation-and-openapi-specification)
- [🔍 Examples](#-examples)
- [🤝 Contributing](#-contributing)
- [🧪 Testing](#-testing)
- [📬 Contact](#-contact)

---

## ✨ Features

- ✅ Full CRUD operations for **events**, **passes**, **teams**, and **users**.
- 📖 Interactive API documentation via **Swagger-UI** and **ReDoc** (FastAPI auto-generation feature).
- 🧩 Seamless integration with **OpenAPI** (3.1) for schema validation.
- ⚡ Fast and scalable powered by the **FastAPI** framework.
- 🔧 Designed for ease of **modification** and **long-term maintainability**.

## ⚙️ Installation

Follow these steps to run the Fest-API:

```shell
# Clone the repository.
git clone https://github.com/k-srivastava/Fest-API.git

# Navigate into the project directory.
cd Fest-API

# Create and activate a virtual environment.
python -m venv .venv
source .venv/bin/activate  # For Windows: .\.venv\Scripts\activate

# Install the required dependencies.
pip install -r requirements.txt

# (Optional) Set the environment variables (e.g., the database URL).
export DATABASE_URL=<your-database-url>
```

---

## 🚀 Getting Started with the API

1. Run the API server using `uvicorn`.
    ```shell
    uvicorn main:app --reload
    ```

2. Visit the interactive documentation.
   Visit the endpoints below in your browser:
    - **Swagger-UI**: `http://127.0.0.1:8000/docs`
    - **ReDoc**: `http://127.0.0.1:8000/redoc`

You can start exploring and testing the API interactively right away!

---

## 📜 Documentation and OpenAPI Specification

This API adheres to the **OpenAPI Specification**. The schema is auto-generated and accessible at `/openapi.json`.

### Key Endpoints

| **Endpoint**       | **Method** | **Description**                 |
|--------------------|------------|---------------------------------|
| `/event/`          | `GET`      | Fetch all events.               |
| `/pass/`           | `GET`      | Fetch user passes.              |
| `/team/{team_id}/` | `GET`      | Fetch information about a team. |
| `/user/{user_id}/` | `GET`      | Fetch user-specific data.       |

You can test the endpoints either in Swagger-UI or using a REST client like Postman.

---

## 🔍 Examples

### Example: Retrieve All Events

#### Request:

```shell
curl -X GET "http:://127.0.0.1:8000/events" -H "accept: application/json"
```

#### Example Response:

```json
[
  {
    "name": "Hackathon 2024",
    "description": "A 48-hour coding event!",
    "type": "technical",
    "team_members": 5,
    "start": "2025-01-01T10:00:00",
    "venue": "MIT Auditorium",
    "id": 1
  },
  "..."
]
```

---

## 🤝 Contributing

Fest-API is always open to contributions. Feel free to open an issue or create a pull request. For major changes, please
open an issue first to discuss, and we will get back to you shortly either online or in person.


---

## 🧪 Testing

The API is extensively tested at all endpoints using Python's built-in **unittest** library. Run the tests:

```shell
python tests/test_suite.py
```

## 📬 Contact

- **Email**: **kshitijsrivastava2312@gmail.com**
- Create an issue on the repository for bug reports or features.
