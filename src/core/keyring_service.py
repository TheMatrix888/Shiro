from base64 import urlsafe_b64encode
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from keyring import delete_password, get_password, set_password


class KeyringService:
    def __init__(self, service_name: str, password: str, salt: bytes):
        self.service_name = service_name
        self.fernet = Fernet(self._generate_key(password, salt))

    @staticmethod
    def _generate_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000
        )
        return urlsafe_b64encode(kdf.derive(password.encode()))

    def set_password(self, username: str, password: str) -> None:
        encrypted_password = self.fernet.encrypt(password.encode())
        set_password(self.service_name, username, encrypted_password.decode())

    def get_password(self, username: str) -> Optional[str]:
        encrypted_password = get_password(self.service_name, username)
        if encrypted_password is None:
            return None
        try:
            return self.fernet.decrypt(encrypted_password.encode()).decode()
        except InvalidToken:
            raise ValueError("Failed to decrypt password. Invalid encryption key.")

    def delete_password(self, username: str) -> None:
        delete_password(self.service_name, username)
