# Handles public form submission (User role only)
from fastapi import APIRouter,Depends,HTTPException,status,Request
from dataModels import CurrentUser,FormDetails
from .auth import getCurrentUser
from limiter import limiter

router = APIRouter()

# Dependency: Check if the user has the 'user' role
# This acts as a Gatekeeper for endpoints using it
@router.get("/formAccess",response_model=CurrentUser)
@limiter.limit("5/2minute") # Rate limit: 5 requests per 2 minutes
def formAccess(request: Request, user : CurrentUser = Depends(getCurrentUser)):
    if user.role != "user":
        # Reject if not 'user' role
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only User Can Submit Forms",headers={"WWW-Authenticate":"Bearer"})
    return user

# Endpoint: Submit form data
# Uses 'formAccess' dependency to ensure only 'user' role can access
@router.post("/submitForm",response_model=FormDetails)
@limiter.limit("5/2minute") # Rate limit logic applied here
def submitForm(request: Request, formData : FormDetails,user : CurrentUser = Depends(formAccess)):
    # If code reaches here, Authentication (valid token) and Authorization (role check) passed
    return formData
