import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken


def derive_key(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt_message(message: str, password: str) -> str:
    key = derive_key(password)
    cipher = Fernet(key)
    return cipher.encrypt(message.encode()).decode()


def decrypt_message(token: str, password: str) -> str:
    key = derive_key(password)
    cipher = Fernet(key)

    try:
        return cipher.decrypt(token.encode()).decode()
    except InvalidToken:
        raise ValueError("Wrong password or corrupted message")