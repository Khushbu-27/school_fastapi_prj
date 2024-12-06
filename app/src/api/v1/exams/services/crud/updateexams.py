
from datetime import datetime
from sqlalchemy.orm import Session
from app.src.api.v1.exams.services.crud.createexams import Exam
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user
from fastapi import HTTPException, status
from app.src.api.v1.utils.response_utils import Response


class examupdateservices:
    
    #TEACHER UPDATE EXAM SCHEDULE
    def update_exam_schedule(exam_id: int,date: str,status: str ,marks: int ,db: Session,
        # test_paper: UploadFile = File(None),  
        current_user = authorize_user,  
    ):
        
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Only teachers can update exams.")
        
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        if current_user.class_name != exam.class_name or current_user.subject_name != exam.subject_name:
            raise HTTPException(status_code=403, detail="You cannot update an exam for this class or subject.")
        
        try:
            exam_date = datetime.strptime(date, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use DD-MM-YYYY.")
        
        if exam_date < datetime.today().date():
            raise HTTPException(status_code=400, detail="Exam date cannot be in the past.")
        
        if status:
            status = status.lower()
            if status not in ['scheduled', 'completed']:
                raise HTTPException(status_code=400, detail="Invalid status. Choose either 'scheduled' or 'completed'.")

        if status:
            exam.status = status
        if marks is not None:
            exam.marks = marks
        exam.date = exam_date

        # if test_paper:
            
        #     old_file_path = os.path.join(UPLOAD_DIR, exam.test_paper)
        #     if os.path.exists(old_file_path):
        #         os.remove(old_file_path)  

        #     file_name = f"{exam.subject_name}_{exam_date}.pdf" 
        #     file_path = os.path.join(UPLOAD_DIR, file_name)
        #     with open(file_path, "wb") as f:
        #         f.write(test_paper.file.read())

        #     exam.test_paper = file_name

        # Commit the changes to the database
        db.commit()
        
        response_data = {
            "id": exam.id,
            "exam_class": current_user.class_name,  
            "exam_subject": current_user.subject_name,  
            'exam_date': exam.date,
            "exam_status": exam.status,
            "exam_marks": exam.marks,
            # "test_paper": exam.test_paper,  # Include updated test paper filename
            "updated_by": current_user.username 
        }
        
        return Response(
            status_code=200,
            message="Exam updated successfully",
            data=response_data
        ).send_success_response()
