from fastapi import FastAPI
from routers import auth,form,responsesSaved
from limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI()

# Register the Rate Limiter with the main application
app.state.limiter = limiter
# Register the exception handler to return 429 errors properly
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    # Add OWASP recommended security headers
    response.headers["X-Content-Type-Options"] = "nosniff" # Prevent MIME sniffing
    response.headers["X-Frame-Options"] = "DENY" # Prevent Clickjacking
    response.headers["X-XSS-Protection"] = "1; mode=block" # Enable Browser XSS Filter
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains" # Force HTTPS
    # Content Security Policy: Allow assets from self and specific CDNs (for Swagger UI)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data:;"
    return response


# --- STEP 1: ADD CORS MIDDLEWARE ---
# Defines who can talk to this API (Frontend, Mobile App, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (e.g. localhost:5500, myapp.com). Security Warning: Restrict in Production!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers (including Authorization, Content-Type)
)

# Include the routers (micro-apps) for different features
app.include_router(auth.router)
app.include_router(form.router)
app.include_router(responsesSaved.router)

# Simple health check endpoint
@app.get("/sample")
def read_root():
    return {"Hello": "World"}
