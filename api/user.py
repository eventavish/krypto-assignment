from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import utils.auth
from models.model_user import User
from schema.schema_user import UserCreate
from utils import deps

router = APIRouter()


@router.post('/')
async def create_user(user: UserCreate, db: Session = Depends(deps.get_db)):
    if db.query(User).filter(User.email == user.email).first() is not None:
        return JSONResponse(
            status_code=400,
            content={"message": "This username already exists"}
        )

    obj = jsonable_encoder(user)
    obj['hashed_password'] = utils.auth.get_hashed_password(user.password)
    obj.pop('password')
    db_obj = User(**obj)
    db.add(db_obj)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"message": "User created"}
    )


@router.post('/login')
async def login_user(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user is None:
        return JSONResponse(
            status_code=404,
            content={"message": "This username does not exist"}
        )

    if not utils.auth.verify_password(user.password, db_user.hashed_password):
        return JSONResponse(
            status_code=404,
            content={"message": "Incorrect password"}
        )

    return JSONResponse(
        status_code=200,
        content=utils.auth.sign_jwt(user.email)
    )
