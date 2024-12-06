

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.api.v1.marks.models.marksmodel import StudentMarks
from app.src.api.v1.marks.schemas.marksschema import GenerateMarks
from app.src.api.v1.marks.services.crud.createmarks import teachermarksservices
from app.src.api.v1.marks.services.crud.viewmarks import studentmarksservices
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user


teacher_marks_router = APIRouter()
student_marks_router = APIRouter()

@teacher_marks_router.post("/teacher/generate_marks/{exam_id}", tags=['teacher'])
def generate_marks(
        exam_id: int, 
        marks_data: List[GenerateMarks],
        db: Session = Depends(get_db),
        current_user = Depends(authorize_user)
    ):
        return teachermarksservices.generate_marks(exam_id,marks_data,db,current_user)
    
@student_marks_router.get("/students/{student_id}/marks", tags = ["student"])
def get_student_marks(
        student_id: int, 
        db: Session = Depends(get_db), 
        current_user=Depends(authorize_user), 
        response_model=List[StudentMarks]
     ):
        return studentmarksservices.get_student_marks(student_id,db,current_user,response_model)