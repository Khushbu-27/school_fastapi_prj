
from fastapi import FastAPI
from app2.src.api.v1.exam.services.examservices import router

app2 = FastAPI(title="Exam API with mongodb", version="1.0")

app2.include_router(router)

if __name__ == "__main2__":
    import uvicorn
    uvicorn.run(app2, host="127.0.0.1", port=8000)