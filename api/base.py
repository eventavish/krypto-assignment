from fastapi import APIRouter

import api.user
import api.alert

router = APIRouter()

router.include_router(api.user.router, prefix="/user", tags=["user"])
router.include_router(api.alert.router, prefix="/alert", tags=["alert"])
