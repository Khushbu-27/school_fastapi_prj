
from fastapi import APIRouter
from app2.src.api.v1.exam.model.exammodel import Exam
from app2.src.api.v1.exam.schema.examschema import list_serial
from app2.database.database2 import collection_name
from bson import ObjectId

router = APIRouter()

@router.get("/")
def get_exams():
    exams = list_serial(collection_name.find())
    return exams

@router.post("/")
def create_exam(exam:Exam):
    collection_name.insert_one(dict(exam))
    return {"msg":"exam create sucessfully", "exam": exam }

@router.put("/{id}")
def update_exam(id: str, exam: Exam):
    collection_name.find_one_and_update({"_id":ObjectId(id)},{"$set": dict(exam)})
    return {"msg":"exam update sucessfully", "exam": exam }

@router.delete("/{id}")
def delete_exam(id: str):
    collection_name.find_one_and_delete({"_id":ObjectId(id)})
    return {"msg":"exam delete sucessfully"}