# handles authentication
# OAuth2 with Password (and hashing), Bearer with JWT tokens
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

import jwt
from jwt.exceptions import InvalidTokenError
from dataModels import User,mockUsers,Token,CurrentUser
from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

router = APIRouter()

# Secret key for signing JWTs (keep this safe in env variables in production)
SECRET_KEY ="187ccc25d4e56e3bbe0f902862efe703d9486301bd89a6e4358dd5238a937a35"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2 #ACCESS TOKENS expire after every 2 minutes

# OAuth2 scheme that extracts the token from the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authorize")
# Password hasher using Argon2 (modern and secure)
password_hash = PasswordHash.recommended()

# Dependency: Decodes the JWT token and retrieves the current user
def getCurrentUser(token : str = Depends(oauth2_scheme)):
    UNAUTHORIZED_ERROR = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",headers={"WWW-Authenticate":"Bearer"})
    try:
        # Decode the token using the secret key
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("username")
        if username is None:
            raise UNAUTHORIZED_ERROR

        # Verify user exists in our "database"
        user_data = mockUsers.get(username)
        if not user_data:
            raise UNAUTHORIZED_ERROR
        return CurrentUser(username=username, role=user_data.role)
    except InvalidTokenError:
        raise UNAUTHORIZED_ERROR

# Helper function to generate a signed JWT
def createJWTTokens(username : str,expireTime : timedelta):
    toEncode={"username":username}
    # Set expiration time (Standard JWT claim 'exp')
    expire=datetime.now(timezone.utc)+expireTime
    toEncode.update({"exp": expire})
    return jwt.encode(toEncode,SECRET_KEY,algorithm=ALGORITHM)

# Login endpoint: Exchanges username/password for a Token
@router.post("/authorize",response_model=Token)
def authorize(formData: OAuth2PasswordRequestForm = Depends()) -> Token:
    UNAUTHORIZED_ERROR = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",headers={"WWW-Authenticate":"Bearer"})
    # Check if user exists
    user:User = mockUsers.get(formData.username)
    if not user:
        raise UNAUTHORIZED_ERROR

    # Verify the provided password against the stored Argon2 hash
    if not password_hash.verify(formData.password,user.hashedPassword):
        raise UNAUTHORIZED_ERROR

    # Generate and return the Access Token
    accessToken = createJWTTokens(user.username,timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=accessToken,token_type="bearer")


# Protected endpoint: Returns the current logged-in user's details
@router.get("/me", response_model=CurrentUser)
def currentUser(user: CurrentUser = Depends(getCurrentUser)):
    return user
