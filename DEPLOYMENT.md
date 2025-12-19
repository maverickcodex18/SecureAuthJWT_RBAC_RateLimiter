# Deployment Guide

## 🚀 Part 1: Deploy Backend (Render)

1.  **Push your code to GitHub** (You already did this!).
2.  **Sign up** at [render.com](https://render.com).
3.  Click **"New +"** -> **"Web Service"**.
4.  Connect your GitHub repository (`SecureAuthJWT_RBAC_RateLimiter`).
5.  **Configure the Service**:
    *   **Name**: `secure-auth-gateway` (or similar)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
6.  Click **"Create Web Service"**.
7.  Wait for it to deploy. Render will give you a URL (e.g., `https://secure-auth-gateway.onrender.com`).

**✅ Success!** Your backend is now live on the cloud.

---

## 🌐 Part 2: Deploy Frontend (GitHub Pages)

1.  **Edit `index.html`**:
    You need to tell your frontend where the *live* backend is.
    Change `API_BASE` from localhost to your Render URL:
    ```javascript
    // const API_BASE = "http://127.0.0.1:8000"; // OLD (Local)
    const API_BASE = "https://secure-auth-gateway.onrender.com"; // NEW (Cloud)
    ```
2.  **Commit and Push** the change to GitHub.
3.  Go to your GitHub Repository -> **Settings** -> **Pages**.
4.  Under **Source**, select `main` branch and `/ (root)` folder.
5.  Click **Save**.
6.  GitHub will eventually give you a link (e.g., `https://maverickcodex18.github.io/SecureAuthJWT_RBAC_RateLimiter/`).

**✅ Success!** Your frontend is now live.

---

## ⚠️ Important Notes

*   **CORS**: We already configured `CORSMiddleware` in `main.py` to allow `["*"]`, so your GitHub Pages frontend will be allowed to talk to your Render backend.
*   **Database**: This project uses a **Mock Database** (Response Dictionary). If the Render server restarts (which happens on the free tier), **data will be reset**. For persistence, you would need a real database (PostgreSQL/SQLite).
