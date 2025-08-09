from datetime import datetime, timedelta, timezone
import jwt
import bcrypt as bc
from app.config import settings
from app.models import User


class TokenMaster:
    private_key: bytes = settings.auth.private_key_path.read_bytes()
    public_key: bytes = settings.auth.public_key_path.read_bytes()
    algorithm: str = settings.auth.algorithm

    def __init__(self, token: bytes | None = None, payload: dict | None = None):
        self.token = token
        self.payload = payload

    def encode_payload(
        self,
        data: dict,
        private_key: str | bytes = private_key,
        algorithm: str = algorithm,
    ) -> str:
        return jwt.encode(data, private_key, algorithm)

    def decode_payload(
        self,
        token: str | bytes,
        public_key: str | bytes = public_key,
        algorithm: str = algorithm,
    ) -> dict:
        return jwt.decode(token, public_key, algorithms=[algorithm])


class PasswordMAster:
    @staticmethod
    def hash(password: str) -> bytes:
        return bc.hashpw(
            password=password.encode(),
            salt=bc.gensalt(),
        )

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bc.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )


class AuthService:
    def __init__(self) -> None:
        self.token = TokenMaster()
        self.password = PasswordMAster()

    def _create_jwt_token(
        self,
        user: User,
        expire_minutes: int = 10,
        expire_timedelta: timedelta | None = None,
    ):
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        return self.token.encode_payload(
            data={
                "sub": str(user.id),
                "username": user.username,
                "iat": now,
                "exp": expire,
            }
        )
    def create_acces_token(self, *args, **kwargs):
        kwargs["expire_minutes"] = settings.auth.access_token_expire_minets  
        return self._create_jwt_token(*args, **kwargs)

    def create_refresh_token(self, *args, **kwargs):
        kwargs["expire_timedelta"] = settings.auth.refresh_token_expire
        return self._create_jwt_token(*args, **kwargs)



auth_service = AuthService()
