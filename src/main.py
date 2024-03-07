from fastapi import FastAPI

from src.controllers import routers

app = FastAPI(title="Blockchain API", version="0.1.0")

for router in routers:
    app.include_router(router)
