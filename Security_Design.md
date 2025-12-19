# System & Security Architecture Documentation

## 1. Authentication Architecture (OAuth2 + JWT)
The system implements a standardized **OAuth2 Password Flow** with Bearer Token authentication. This stateless design allows for horizontal scalability while maintaining strict security.

### A. Password Handling (At Rest)
*   **Hashing Algorithm**: `Argon2id`
*   **Implementation**: Via `pwdlib` (modern wrapper for `argon2-cffi`).
*   **Configuration**:
    *   `v=19`: Algorithm version.
    *   `m=65536`: 64MB memory cost (makes GPU/ASIC cracking expensive).
    *   `t=3`: 3 iterations (linear time cost).
    *   `p=4`: 4 degrees of parallelism.
*   **Process**: Passwords are *never* stored plain-text. They are verified using `password_hash.verify(secret, stored_hash)`.

### B. Token Lifecycle (In Transit)
*   **Format**: JSON Web Token (JWT) signed with `Generic (HS256)` HMAC-SHA256.
*   **Payload Claims**:
    *   `sub` (or custom `username`): Identity of the user.
    *   `exp`: Expiration timestamp (set to 5 minutes to force frequent re-auth).
*   **Transport**: Tokens are passed in the `Authorization` header: `Bearer <token>`.

---

## 2. Component Security Analysis

### A. Authentication Router (`routers/auth.py`)
*   **Responsibility**: Identity verification and Token vending.
*   **Security Controls**:
    *   **Cryptographic Verification**: Validates user credentials against stored Argon2 hashes.
    *   **User Lookup**: Retrieves user role and data securely.
    *   **Token Minting**: Generates signed JWTs.
    *   **The `/me` Endpoint**: Validates the token to return the current user's context.

### B. Public Form Router (`routers/form.py`)
*   **Responsibility**: Data ingestion from standard users.
*   **RBAC Policy**: `Role = "user"`.
    *   Implemented via `Depends(formAccess)`.
    *   Strictly rejects "admin" or unauthenticated requests with `403 Forbidden`.
*   **DoS Protection**: Rate-limited to **5 requests / 2 minutes** per IP.

### C. Admin Responses Router (`routers/responsesSaved.py`)
*   **Responsibility**: Sensitive data retrieval.
*   **RBAC Policy**: `Role = "admin"`.
    *   Implemented via `Depends(responsesAccess)`.
    *   Ensures segregation of duties; standard users cannot harvest data.
*   **DoS Protection**: Rate-limited to **5 requests / 2 minutes**.

---

## 3. Input Validation & Data Integrity
The application relies on **Pydantic** for rigorous schema enforcement.

*   **Strict Typing**: All inputs (`UserLogin`, `FormDetails`) have defined types (`str`, `int`).
*   **Automatic Sanitization**: Pydantic strips unknown fields by default, preventing "Mass Assignment" vulnerabilities.
*   **Validation Errors**: Invalid requests are rejected immediately with `422 Unprocessable Entity`, preventing malformed data from reaching business logic.

---

## 4. Security Middleware (OWASP and Rate Limiter) & Defense in Depth

### A. Rate Limiting (`limiter.py`)
*   **Strategy**: "Defense in Depth" against brute-force and exhaustion attacks.
*   **Implementation**: `SlowAPI` (Redis-ready implementation of `limits`).
*   **Scope**: Applied to login checks, form submissions, and data retrieval.

### B. Security Headers (Middlewares OWASP)
Every HTTP response is hardened with the following OWASP-recommended headers:

| Header | Value | Purpose |
| :--- | :--- | :--- |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Forces browsers to use HTTPS only. |
| `X-Content-Type-Options` | `nosniff` | Prevents browsers from "guessing" (sniffing) MIME types. |
| `X-Frame-Options` | `DENY` | Prevents Clickjacking by disallowing framing. |
| `X-XSS-Protection` | `1; mode=block` | Enables legacy browser XSS filters. |
| `Content-Security-Policy` | `default-src 'self' ...` | Restricts sources of Scripts, CSS, and Images to trusted origins. |

---

## 5. API Security Best Practices Checklist

| Practice | Status | Implementation Details |
| :--- | :---: | :--- |
| **Use HTTPS** | ✅ | Enforced via HSTS header (requires deployment behind TLS proxy). |
| **Use Hash Algorithms** | ✅ | Argon2id used for password storage. |
| **Never pass secrets in URL** | ✅ | Credentials passed in POST body; Token in Header. |
| **Validate Input** | ✅ | Full Pydantic schema validation. |
| **Limit Rate** | ✅ | 5 req/2min limit on sensitive endpoints. |
| **Least Privilege** | ✅ | Separate Admin/User roles enforcing strict access boundaries. |
| **Standard Error Messages** | ✅ | Unified HTTP 401/403/422 responses. |
