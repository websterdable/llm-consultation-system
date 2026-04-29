from app.core.security import create_access_token, decode_token, hash_password, verify_password


def test_hash_and_verify_password():
    password = "securepass123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)


def test_create_and_decode_token():
    data = {"sub": "42", "role": "user"}
    token = create_access_token(data)
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload