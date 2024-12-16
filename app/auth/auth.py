from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy


def get_jwt_strategy(secret_key: str) -> JWTStrategy:
    return JWTStrategy(secret=secret_key, lifetime_seconds=3600)


cookie_transport = CookieTransport(cookie_name="TODOes", cookie_max_age=3600)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
