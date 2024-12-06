
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.api.v1.exams.services.crud.viewexams import Exam
from app.src.api.v1.marks.schemas.marksschema import StudentMarks
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user
from app.src.api.v1.utils.response_utils import Response


class studentmarksservices:

    #STUDENT VIEW OWN MARKS
    def get_student_marks(student_id: int, db: Session, current_user=authorize_user, response_model=List[StudentMarks]):

        if current_user.role != "student" or current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Access forbidden")

        eligible_exams = db.query(Exam).filter(Exam.class_name == current_user.class_name).all()
        if not eligible_exams:
            raise HTTPException(status_code=403, detail="You are not authorized to view this exam marks.")
        
        marks_records = (
            db.query(
                StudentMarks.id,
                StudentMarks.student_name,
                StudentMarks.class_name,
                StudentMarks.subject_name,
                StudentMarks.student_marks.label("student_marks"),
                Exam.date
            )
            .join(Exam, StudentMarks.exam_id == Exam.id)
            .filter(StudentMarks.student_name == current_user.username)
            .all()
        )

        if not marks_records:
            raise HTTPException(status_code=404, detail="Marks not found for the student")

        return Response(
            data=[
                {
                    "id": record.id,
                    "student_name": record.student_name,
                    "class_name": record.class_name,
                    "subject_name": record.subject_name,
                    "student_marks": record.student_marks,
                    "exam_date": record.date,
                }
                for record in marks_records
            ],
            status_code=200,
            message="Student marks details retrieved successfully"
        ).send_success_response()


        
