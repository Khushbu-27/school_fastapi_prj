

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.api.v1.exams.services.crud.createexams import teacherexamservices
from app.src.api.v1.exams.services.crud.deleteexams import examdeleteservices
from app.src.api.v1.exams.services.crud.updateexams import examupdateservices
from app.src.api.v1.exams.services.crud.viewexams import examviewservices
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user


teacher_exam_router = APIRouter()


@teacher_exam_router.post("/teacher/add_exam/paper_s3_bucket", tags=["Exam"])
def add_exam_and_paper_in_s3bucket(
        date: str = Query(...),
        status: str = Query(...),
        marks: int = Query(...),
        test_paper: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user:User=Depends(authorize_user),
    ):
        return teacherexamservices.add_exam_and_paper_in_s3bucket(date,status,marks,test_paper,db,current_user)
    
@teacher_exam_router.get("/teacher-student/view_exam/{exam_id}", tags=["Exam"])
def view_exam_schedule(
        # request: Request,
        exam_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(authorize_user)
    ):
        return examviewservices.view_exam_schedule(db,exam_id,current_user)
        
@teacher_exam_router.get("/teacher/view_testpaper/{exam_id}", tags=["Exam"])
def view_testpaper_from_s3(
        exam_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(authorize_user),
    ):
        return examviewservices.view_testpaper_from_s3(exam_id,db,current_user)
    
@teacher_exam_router.put("/teacher/update_exam/{exam_id}", tags=["Exam"])
def update_exam_schedule(
        exam_id: int,
        db: Session = Depends(get_db),
        date: str = Query(...),
        status: str = None,
        marks: int = None,
        # test_paper: UploadFile = File(None),  
        current_user = Depends(authorize_user),
        
    ):
        return examupdateservices.update_exam_schedule(exam_id,db,date,status,marks,current_user)
    
@teacher_exam_router.delete("/teacher/delete_exam/{exam_id}" , tags=['Exam'])
def delete_exam(exam_id: int, current_user=Depends(authorize_user), db: Session = Depends(get_db)):
        return examdeleteservices.delete_exam(exam_id,db,current_user)