"""JWT authentication endpoints"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from ninja import Router
from ninja_jwt.tokens import RefreshToken

from pyticket.entrypoints.web.api.auth.schemas import TokenResponseSchema, UserLoginSchema, UserRegistrationSchema

User = get_user_model()

router = Router(tags=["auth"])


@router.post("/register", response={200: TokenResponseSchema, 400: dict})
def register(request, payload: UserRegistrationSchema):
    """
    Register a new user and return JWT tokens.

    This endpoint allows new users to create an account and immediately
    receive JWT tokens for authentication.
    """
    # Check if user already exists
    if User.objects.filter(username=payload.username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    # Validate password
    try:
        validate_password(payload.password)
    except ValidationError as e:
        return JsonResponse({"error": "; ".join(e.messages)}, status=400)

    # Create user
    user = User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email if payload.email else "",
    )

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        "access": access_token,
        "refresh": refresh_token,
    }


@router.post("/login", response={200: TokenResponseSchema, 401: dict})
def login(request, payload: UserLoginSchema):
    """
    Login with username and password to get JWT tokens.

    This endpoint is provided by NinjaJWTDefaultController, but we're
    creating a custom one for consistency with our registration endpoint.
    """
    from django.contrib.auth import authenticate

    user = authenticate(username=payload.username, password=payload.password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        "access": access_token,
        "refresh": refresh_token,
    }
