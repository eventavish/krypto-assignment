from typing import Generator, Optional
from fastapi import FastAPI, Depends, Header
from sqlalchemy.orm import Session

import utils.auth
from db.session import SessionLocal
from models.model_user import User

app = FastAPI()


def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)) -> Optional[User]:
    decoded = utils.auth.decode_jwt(authorization)
    if decoded is None:
        return None

    return db.query(User).filter(User.email == decoded['email']).first()
