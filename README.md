# SecureAuth RBAC RateLimiter Gateway

A robust, security-focused API Gateway built with **FastAPI**. This project demonstrates enterprise-grade security patterns including OAuth2 Authentication, Role-Based Access Control (RBAC), Rate Limiting, and Defense-in-Depth security headers.

## 🚀 Key Features

*   **Authentication**: OAuth2 Password Flow with stateless **JWT** (JSON Web Tokens). **Tokens expire in 2 minutes** to enforce security.
*   **Password Security**: Industry-standard **Argon2** hashing via `pwdlib`.
*   **Access Control (RBAC)**: Granular permission checks for **Admin** and **User** roles.
*   **DoS Protection**: Rate Limiting using **SlowAPI** (Token Bucket algorithm).
*   **Security Hardening**: Custom Middleware injecting **OWASP** recommended headers (HSTS, CSP, X-Frame-Options, etc.).
*   **Input Validation**: Strict schema enforcement using **Pydantic**.

## 🛠️ Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone git@github.com:maverickcodex18/SecureAuthJWT_RBAC_RateLimiter.git
    cd SecureAuth_RBAC_RateLimiter_Gateway
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```bash
    fastapi dev main.py
    ```

5.  **Run the Frontend**:
    Simply open `index.html` in your browser.
    *   **WSL**: `explorer.exe index.html`
    *   **Windows/Linux**: Double click the file.

The server will start at `http://127.0.0.1:8000`.

## 📚 Documentation

*   **Swagger UI**: Visit `http://127.0.0.1:8000/docs` for interactive API testing.
*   **System Design**: See [System_Security_Design.md](System_Security_Design.md) for architectural details.
*   **Request Flow**: See [Client_Server_Flow.md](Client_Server_Flow.md) for a visual breakdown of the request lifecycle.
*   **Learning Resources**: See [Learning.md](Learning.md) for tutorials on the tech stack.

## 📂 Project Structure

*   `main.py`: Entry point, App initialization, and Security Middleware.
*   `limiter.py`: Centralized Rate Limiter configuration.
*   `dataModels.py`: Pydantic schemas and Mock Database.
*   `routers/`:
    *   `auth.py`: Login and Token generation logic.
    *   `form.py`: User-facing endpoints (RBAC: User).
    *   `responsesSaved.py`: Admin-facing endpoints (RBAC: Admin).
*   `index.html`: Client-side frontend for testing Authentication, RBAC, and Rate Limiting visually.

## 🧪 Default Credentials (Mock DB)

| Role | Username | Password | Access |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Full access, including `/responses` |
| **User** | `user` | `user123` | Can submit forms via `/submitForm` |


## Deployment Link

(SecureAuth RBAC RateLimiter Gateway)
Live Demo Link : https://github.com/maverickcodex18/SecureAuthJWT_RBAC_RateLimiter/deployments/github-pages
