import pytest
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.jwt import decode_and_validate
from app.core.config import settings

def create_test_token(sub="42", role="user"):
    payload = {
        "sub": sub,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)

def test_decode_valid_token():
    token = create_test_token()
    payload = decode_and_validate(token)
    assert payload["sub"] == "42"
    assert payload["role"] == "user"

def test_decode_invalid_token():
    with pytest.raises(ValueError):
        decode_and_validate("garbage.token.here")

def test_decode_expired_token():
    payload = {
        "sub": "42",
        "role": "user",
        "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
    with pytest.raises(ValueError):
        decode_and_validate(token)