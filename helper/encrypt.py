from passlib.hash import sha256_crypt
from jose import jwt
from config import encryption_config

def encrypt_password(password: str) -> str:
    return sha256_crypt.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    return sha256_crypt.verify(password, hashed_password)


def create_token(id: int) -> str:
    token = jwt.encode(
        {"id": id},
        encryption_config["SECRET_KEY"],
        encryption_config["ALGORITHM"]
    )
    return token
