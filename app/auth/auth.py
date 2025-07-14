import jwt
import bcrypt as bc
from app.config import settings


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
    def hash_password(password: str) -> bytes:
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


class AuthManager:
    def __init__(self) -> None:
        self.token = TokenMaster()
        self.password = PasswordMAster()


auth_manager = AuthManager()
