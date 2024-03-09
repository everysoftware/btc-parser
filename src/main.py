from fastapi import FastAPI

from src.controllers import routers

app = FastAPI(title="BTC Parser")

for router in routers:
    app.include_router(router)
