
import os
from fastapi import FastAPI
from app.blueprints.routers import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="School mangement API", version="1.0")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("APP_HOST"), port=os.getenv("APP_PORT"))
