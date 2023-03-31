DB_NAME_AND_USER: str = ""
DB_PASS: str = ""
DB_HOST: str = ""
SECRET_KEY: str = ""
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_WEEKS: int = 52
JWT_OPTIONS: dict[str, bool | int] = {
    "verify_signature": True,
    "verify_aud": True,
    "verify_iat": True,
    "verify_exp": True,
    "verify_nbf": True,
    "verify_iss": True,
    "verify_sub": False,
    "verify_jti": True,
    "verify_at_hash": True,
    "require_aud": False,
    "require_iat": False,
    "require_exp": False,
    "require_nbf": False,
    "require_iss": False,
    "require_sub": False,
    "require_jti": False,
    "require_at_hash": False,
    "leeway": 0,
}
