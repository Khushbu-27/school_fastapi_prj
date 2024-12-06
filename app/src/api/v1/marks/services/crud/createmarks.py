

from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.api.v1.exams.services.crud.viewexams import Exam
from app.src.api.v1.marks.schemas.marksschema import GenerateMarks, GeneratedMarkResponse, StudentMarks
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user
from app.src.api.v1.utils.response_utils import Response


class teachermarksservices:

    #TEACHER GENERATE STUDENT MARKS
    def generate_marks(exam_id: int, marks_data: List[GenerateMarks],db: Session,current_user = authorize_user):

        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Only teachers can generate marks")

        exam = db.query(Exam).filter(
            Exam.id == exam_id
        ).first()

        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found.")

        if exam.class_name != current_user.class_name :
            raise HTTPException(status_code=403, detail="You cannot generate marks for this class or subject.")
        response_data = []  

        for mark in marks_data:
            
            student = db.query(authorize_user).filter(
                authorize_user.username == mark.student_name,
                authorize_user.class_name == exam.class_name,
                # models.User.subject_name == exam.subject_name
            ).first()

            if not student:
                raise HTTPException(status_code=404, detail=f"Student '{mark.student_name}' not found in class {exam.class_name}.")

            existing_marks = db.query(StudentMarks).filter(
                StudentMarks.student_name == mark.student_name,
                StudentMarks.exam_id == exam.id
            ).first()

            if existing_marks:
                raise HTTPException(status_code=400, detail=f"Marks for student '{mark.student_name}' have already been added for this exam.")
            
            if exam.date >= datetime.today().date():
                raise HTTPException(status_code=400, detail="Exam is not completed yet.You can not add marks")

            if mark.student_marks > exam.marks:
                raise HTTPException(status_code=400, detail=f"Marks cannot be greater than the maximum marks ({exam.marks}) for this exam.")

            new_marks = StudentMarks(
                student_name=mark.student_name, 
                class_name=exam.class_name,
                subject_name=exam.subject_name, 
                exam_id=exam.id,        
                student_marks=mark.student_marks        
            )
            db.add(new_marks)

            response_data.append(GeneratedMarkResponse(
                exam_id=exam.id,
                student_name=mark.student_name,
                class_name=exam.class_name,
                subject_name=exam.subject_name,
                marks=mark.student_marks
            ))

        db.commit()
        
        return Response(
            status_code=200,
            message="Student marks added successfully",
            data= response_data 
        ).send_success_response()