
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from requests import post
from app.blueprints.routers import router

app = FastAPI(title="School mangement API", version="1.0")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



