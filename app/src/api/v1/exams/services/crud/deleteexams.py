
import boto3
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.api.v1.exams.services.crud.viewexams import Exam
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user
from app.src.api.v1.utils.response_utils import Response
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.exams.config.awsconfig import AWS_ACCESS_KEY_ID, AWS_BUCKET_NAME, AWS_REGION, AWS_SECRET_ACCESS_KEY 

# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#     region_name=AWS_REGION,
# )

class examdeleteservices:


    #TEACHER DELETE EXAM
    def delete_exam(exam_id: int, db: Session, current_user: User):
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Only teachers can delete exams.")
        
        teacher_name = current_user.username
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found.")
        
        if exam.teacher_name != teacher_name:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this exam schedule.")
        
        if exam.class_name != current_user.class_name or exam.subject_name != current_user.subject_name:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this exam schedule for this class/subject.")
    
        # try:
        #     file_key = exam.test_paper.split(f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/")[-1]
            
        #     s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=file_key)
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=f"Failed to delete test paper from S3: {str(e)}")

        db.delete(exam)
        db.commit()
        
        response_data = {
            "id": exam.id,
            "exam_class": exam.class_name,
            "exam_subject": exam.subject_name,
            "exam_date": exam.date,
            "marks": exam.marks,
            "added_by": teacher_name
        }
        
        return Response(
            status_code=200,
            message="Exam and associated test paper deleted successfully.",
            data=response_data
        ).send_success_response()

        # Construct the file path to the test paper
        # file_path = os.path.join(UPLOAD_DIR, exam.test_paper)
        
        # Ensure the file exists before trying to delete
        # if os.path.exists(file_path):
        #     os.remove(file_path)  # Delete the file
        # else:
        #     # If the file does not exist, raise an error indicating it's missing
        #     raise HTTPException(status_code=404, detail="Test paper file not found in storage")