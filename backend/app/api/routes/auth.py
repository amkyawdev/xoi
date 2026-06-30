from fastapi import APIRouter, HTTPException, Depends
from app.api.models.request_models import LoginRequest, RegisterRequest, ResetPasswordRequest
from app.api.models.response_models import AuthResponse, UserResponse
from app.services.auth_service import AuthService
from datetime import datetime

router = APIRouter()

async def get_auth_service():
    return AuthService()

@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        result = await service.login(request.email, request.password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return AuthResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        result = await service.register(request.name, request.email, request.password)
        if not result:
            raise HTTPException(status_code=400, detail="Registration failed")
        return AuthResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_password(
    request: ResetPasswordRequest,
    service: AuthService = Depends(get_auth_service)
):
    try:
        result = await service.reset_password(request.email)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "Password reset email sent"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
