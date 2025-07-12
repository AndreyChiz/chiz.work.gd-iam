import jwt
from app.config import settings

class TokenJWT:
    private_key: bytes = settings.auth_jwt.private_key_path.read_bytes()
    public_key: bytes = settings.auth_jwt.public_key_path.read_bytes()
    algorithm: str = settings.auth_jwt.algorithm

    def __init__(self, token: bytes | None = None, payload: dict | None = None):
        self.token = token
        self.payload = payload

    def encode_data(
        self,
        data: dict,
        private_key: str| bytes=private_key,
        algorithm: str=algorithm,
    ) -> str:
        return jwt.encode(data, private_key, algorithm)

    def decode_token(
        self,
        token: str | bytes,
        public_key: str| bytes=public_key,
        algorithm: str =algorithm,
    ) -> dict:
        return jwt.decode(token, public_key, algorithms=[algorithm])
