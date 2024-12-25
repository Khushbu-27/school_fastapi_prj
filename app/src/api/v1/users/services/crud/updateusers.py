

from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.schemas.userschemas import TeacherSalary, UserUpdate
from app.src.api.v1.users.services.user_authentication.user_auth import get_password_hash
from app.src.api.v1.utils.response_utils import Response


class adminupdateservices:

    # ADMIN UPDATE OWN INFO
    def admin_update_own_info(update_data: UserUpdate, db: Session, current_user = User):

        admin = db.query(User).filter(User.username == current_user.username).first()
        
        if not admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin authorization required")
        
        if update_data.password:
            admin.hashed_password = get_password_hash(update_data.password)
        db.commit()
        db.refresh(admin)
        response_data = {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "password": admin.hased_password
        }
        return Response(
            status_code=200,
            message="Admin detail updated successfully",
            data= response_data 
        ).send_success_response()


    # ADMIN UPDATE TEACHER SALARY
    def admin_update_teacher_salary(teacher_id: int,db: Session ,current_user:User,salary: TeacherSalary):
        
        
        # teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
        teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()

        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        if teacher.salary is None:
            raise HTTPException(status_code=400, detail="Teacher salary must be set first before updating")

        teacher.salary = salary.salary
        db.commit()
        db.refresh(teacher)

        response_data = {
            "id": teacher.id,
            "username": teacher.username,
            "salary":teacher.salary
        }
        return Response(
            status_code=200,
            message="Teacher salary updated successfully",
            data= response_data 
        ).send_success_response()
    
    
class teacherupdateservices:
    
    # TEACHER UPDATE OWN INFO
    def teacher_update_own_info(update_data: UserUpdate, db: Session, current_user = User):

        if current_user.role != "teacher":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher authorization required")
        
        teacher = db.query(User).filter(User.username == current_user.username).first()
        # if update_data.username:
        #     teacher.username = update_data.username
        if update_data.password:
            teacher.hashed_password = get_password_hash(update_data.password)
        db.commit()
        db.refresh(teacher)
        response_data = {
            "id": teacher.id,
            "username": teacher.username,
            "email":teacher.email,
            "password": teacher.hased_password
        }
        return Response(
            status_code=200,
            message="Teacher detail updated successfully",
            data= response_data 
        ).send_success_response()
        
class studentupdateservices:
    
    # STUDENT UPDATE OWN INFO
    def student_update_own_info(update_data: UserUpdate, db: Session ,current_user = User):

        if current_user.role != "student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student authorization required")
        
        student = db.query(User).filter(User.username == current_user.username).first()
        # if update_data.username:
        #     student.username = update_data.username
        if update_data.password:
            student.hashed_password = get_password_hash(update_data.password)
        db.commit()
        db.refresh(student)
        response_data = {
            "id": student.id,
            "username": student.username,
            "email": student.email,
            "password": student.hased_password
        }
        return Response(
            status_code=200,
            message="Student detail updated successfully",
            data= response_data 
        ).send_success_response()