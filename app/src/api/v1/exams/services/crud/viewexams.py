
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.src.api.v1.exams.models.exammodel import Exam
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user
from app.src.api.v1.utils.response_utils import Response


class examviewservices:
    
    #TEACHER,STUDENT VIEW EXAM SCHEDULE
    def view_exam_schedule(request: Request,exam_id: int,db: Session ,current_user: User= authorize_user):
        
        if current_user.role not in ["student", "teacher"]:
            raise HTTPException(status_code=403, detail="Only students and teachers can view exam schedules.")

        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found.")

        if current_user.role == "teacher":
            if exam.class_name != current_user.class_name or exam.subject_name != current_user.subject_name:
                raise HTTPException(status_code=403, detail="You are not authorized to view this exam schedule.")
        
        elif current_user.role == "student":
            if exam.class_name != current_user.class_name:
                raise HTTPException(status_code=403, detail="You are not authorized to view this exam schedule.")

        # file_name = exam.test_paper  

        # base_url = request.base_url  
        # download_file_url = f"{base_url}static/{file_name}" 
        
        s3_url = exam.test_paper 

        response_data = {
            "id": exam.id,
            "exam_class": exam.class_name,
            "exam_subject": exam.subject_name,
            "exam_date": exam.date,
            "exam_marks": exam.marks,
            "file_path": s3_url,  
        }
        return Response(
            status_code=200,
            message="Exam details retrieved successfully",
            data=response_data
        ).send_success_response()
        
        
    #TEACHER VIEW EXAM PAPER FROM S3    
    def view_testpaper_from_s3(
        exam_id: int,
        db: Session ,
        current_user: authorize_user,
    ):
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=403, 
                detail="Only teachers can view or download files."
            )

        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=404, 
                detail="Exam not found in the database."
            )

        if exam.teacher_name != current_user.username:
            raise HTTPException(
                status_code=403, 
                detail="You are not authorized to view this file."
            )

        s3_url = exam.test_paper
        return JSONResponse(content={"url": s3_url})