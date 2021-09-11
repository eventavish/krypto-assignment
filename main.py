import uvicorn
from fastapi import FastAPI

import api.base
import celery_worker.alert_monitor

app = FastAPI()
app.include_router(api.base.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)
