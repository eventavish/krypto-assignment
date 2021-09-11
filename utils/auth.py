import binascii
import time
from typing import Dict, Optional

import bcrypt as bcrypt
import jwt

import config.settings


def get_hashed_password(plain_text_password: str):
    raw = bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())
    return binascii.hexlify(raw).decode()


def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_text_password.encode(), binascii.unhexlify(hashed_password))


def sign_jwt(username: str) -> Dict[str, str]:
    payload = {
        'username': username,
        'expires': time.time() + 3600
    }

    token = jwt.encode(payload, config.settings.JWT_SIGNING_KEY, algorithm=config.settings.JWT_SIGNING_ALGORITHM)
    return {
        'access_token': token
    }


def decode_jwt(token: str) -> Optional[dict]:
    try:
        decoded_token = jwt.decode(token, config.settings.JWT_SIGNING_KEY,
                                   algorithms=[config.settings.JWT_SIGNING_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None
