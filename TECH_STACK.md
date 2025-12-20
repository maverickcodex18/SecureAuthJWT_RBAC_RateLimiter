# 🛠️ Technology Stack & Tools

This project is built using a modern, security-focused stack designed for performance and scalability.

## 🐍 Backend (Python)

| Component | Tool/Library | Purpose |
| :--- | :--- | :--- |
| **Framework** | **[FastAPI](https://fastapi.tiangolo.com/)** | High-performance async web framework for building APIs. |
| **Server** | **[Uvicorn](https://www.uvicorn.org/)** | ASGI web server implementation for Python. |
| **Data Validation** | **[Pydantic](https://docs.pydantic.dev/)** | Data validation and settings management using Python type hints. |
| **Rate Limiting** | **[SlowAPI](https://pypi.org/project/slowapi/)** | Implementation of `limits` for FastAPI to prevent DoS attacks. |

## 🔐 Security & Authentication

| Component | Tool/Library | Purpose |
| :--- | :--- | :--- |
| **Auth Protocol** | **OAuth2** | Industry-standard protocol for authorization (Password Flow). |
| **Token Standard** | **[PyJWT](https://pyjwt.readthedocs.io/)** | Library for encoding, decoding, and verifying JSON Web Tokens (JWT). |
| **Password Hashing** | **[Pwdlib](https://github.com/frankie567/pwdlib) [Argon2]** | Modern password hashing library using the winner of the Password Hashing Competition. |
| **CORS** | **FastAPI CORSMiddleware** | Middleware to control cross-origin resource sharing security. |

## 🎨 Frontend (Client)

| Component | Tool/Library | Purpose |
| :--- | :--- | :--- |
| **Structure** | **HTML5** | Semantic markup for the web interface. |
| **Styling** | **[Tailwind CSS](https://tailwindcss.com/)** | Utility-first CSS framework (via CDN) for rapid UI development. |
| **Scripting** | **Vanilla JavaScript (ES6+)** | Native JS for asynchronous API calls (`fetch`, `async/await`) and DOM manipulation. |
| **Fonts** | **Google Fonts** | "Poppins" font family for typography. |

## ☁️ DevOps & Deployment

| Component | Tool/Library | Purpose |
| :--- | :--- | :--- |
| **Version Control** | **Git** | Distributed version control system. |
| **Backend Hosting** | **[Render](https://render.com/)** | Cloud platform for hosting the Python/FastAPI service. |
| **Frontend Hosting** | **GitHub Pages** | Static hosting for the `index.html` frontend. |
| **API Documentation** | **Swagger UI / OpenAPI** | Auto-generated interactive API docs (built-in to FastAPI). |

## 📦 Dependency Management
*   **`requirements.txt`**: Lists all Python package dependencies.
*   **`pip`**: Python package installer.
