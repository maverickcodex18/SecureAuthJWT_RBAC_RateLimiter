# stores all pydantic models and mock data

from pydantic import BaseModel

# User model for internal representation (fetched from DB/Mock)
class User(BaseModel):
    username: str
    hashedPassword: str # Storing hashed password, never plain text
    role: str

# Model for Login Request Body
class UserLogin(BaseModel):
    username: str
    password: str

# Mock Database simulating a Users table
mockUsers = {
    # Password is 'admin123' hashed with Argon2
    "admin":User(username="admin",hashedPassword="$argon2id$v=19$m=65536,t=3,p=4$hSkP8Py1Ht75EdnvPVLtzA$m//hpvZSvSsLvEOpJIVkr1Dc3ZN2GIOxqWjjbotXh/g",role="admin"),
    # Password is 'user123' hashed with Argon2
    "user":User(username="user",hashedPassword="$argon2id$v=19$m=65536,t=3,p=4$jY+I1OZ46YnY3Sj/Z6y8wQ$D1yB4OBezTTvYaeo294Zx73CR/r3Lup0kA4NssYxLXI",role="user")
}

# Model for the JWT Token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Model for the Current User context (returned by /me)
class CurrentUser(BaseModel):
    username: str
    role: str

# Model for the Form Submission data
class FormDetails(BaseModel):
    age: int
    email: str
    address: str

# Mock Database simulating stored form responses
mockFormDetails = {
    "admin":FormDetails(age=45,email="admin@admin.com",address="Bengaluru,Karnataka"),
    "user":FormDetails(age=18,email="user@user.com",address="Raipur,Chhattisgarh")
}
