from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.model_alert import Alert
from models.model_user import User
from schema import schema_alert
from utils import deps

router = APIRouter()


@router.post('/create')
async def create_alert(alert: schema_alert.Alert, db: Session = Depends(deps.get_db),
                       user: Optional[User] = Depends(deps.get_current_user)):
    if user is None:
        return JSONResponse(
            status_code=403,
            content={'message': 'Unauthorized'}
        )

    obj = jsonable_encoder(alert)
    obj['user_email'] = user.email

    db_obj = Alert(**obj)
    db.add(db_obj)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={'message': 'Alert created'}
    )


@router.delete('/delete/{alert_id}')
async def delete_alert(alert_id: UUID4, db: Session = Depends(deps.get_db),
                       user: Optional[User] = Depends(deps.get_current_user)):
    if user is None:
        return JSONResponse(
            status_code=403,
            content={'message': 'Unauthorized'}
        )

    db_obj = db.query(Alert).filter(Alert.id == alert_id and Alert.user_email == user.email).first()
    if db_obj is None:
        return JSONResponse(
            status_code=404,
            content={'message': 'Alert not found'}
        )

    db.delete(db_obj)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={'message': 'Alert deleted'}
    )


@router.get("/")
async def fetch_alert(db: Session = Depends(deps.get_db),
                      user: Optional[User] = Depends(deps.get_current_user),
                      skip: int = 0, limit: int = 10):
    if user is None:
        return JSONResponse(
            status_code=403,
            content={'message': 'Unauthorized'}
        )

    data = db.query(Alert).filter(Alert.user_email == user.email).offset(skip).limit(limit).all()
    return JSONResponse(
        status_code=200,
        content={'data': jsonable_encoder(data)}
    )
