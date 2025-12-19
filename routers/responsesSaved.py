# Handles Admin-only data retrieval
from fastapi import APIRouter,Depends,HTTPException,status,Request
from dataModels import mockFormDetails,CurrentUser
from .auth import getCurrentUser
from limiter import limiter

router= APIRouter()

# Dependency: RBAC check for 'admin' role
def responsesAccess(user : CurrentUser = Depends(getCurrentUser)):
    if user.role != "admin":
        # Strictly deny access to non-admins
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only Admin Can Access This",headers={"WWW-Authenticate":"Bearer"})
    return user

# Endpoint: Get saved responses
# Protected by 'responsesAccess' ensuring only Admins can invoke this
@router.get("/responses")
@limiter.limit("5/2minute") # Rate limit for Admin actions as well
def getResponses(request: Request, user : CurrentUser = Depends(responsesAccess)):
    return mockFormDetails
