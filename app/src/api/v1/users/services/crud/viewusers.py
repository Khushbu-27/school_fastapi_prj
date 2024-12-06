
from fastapi import HTTPException , status
from sqlalchemy.orm import Session
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.utils.response_utils import Response


class adminviewservices: 
    
    #ADMIN VIEW OWN INFO    
    def admin_view_own_info(admin_id: int, token: dict , db: Session):

        admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()
        if not admin:
            return Response(
                status_code=404,
                message="Admin not found",
                data= {}
            ).send_error_response()
            
        response_data = {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
        }
        return Response(
            status_code=200,
            message="admin details retrieved successfully",
            data= response_data 
        ).send_success_response()
        
        
    #ADMIN VIEW STUDENT INFO
    def admin_view_student_info(student_id: int, token: str , db: Session ):

        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        if not student:
            return Response(
                status_code=404,
                message="Student not found",
                data= {}
            ).send_error_response()
        
        response_data = {
            "id": student.id,
            "username": student.username,
            "email": student.email,
            "class": student.class_name,
        }
        return Response(
            status_code=200,
            message="student details retrieved successfully",
            data= response_data 
        ).send_success_response()


    #ADMIN VIEW TEACHER INFO   
    def admin_view_teacher_info(teacher_id: int, token: str, db: Session):

        teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
        if not teacher:
            return Response(
                status_code=404,
                message="Teacher not found",
                data= {}
            ).send_error_response()
        
        response_data = {
            "id": teacher.id,
            "username": teacher.username,
            "email": teacher.email,
            "class": teacher.class_name,
            "subject": teacher.subject_name,
        }
        return Response(
            status_code=200,
            message="Teacher details retrieved successfully",
            data= response_data 
        ).send_success_response()
        

    #ADMIN VIEW TEACHER SALARY
    def admin_view_teacher_salary(teacher_id: int, db: Session, current_user: User):
    
        teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
        if teacher is None:
            return Response(
                status_code=404,
                message="teacher not found",
                data= {}
            ).send_error_response()

        if teacher.salary is None:
            return Response(
                status_code=404,
                message="Salary not set for this teacher",
                data= {}
            ).send_error_response()

        response_data = {
            "teacher_id": teacher.id, 
            "username": teacher.username,
            "salary": teacher.salary}
        
        return Response(
            status_code=200,
            message="Teacher salary details retrieved successfully",
            data= response_data 
        ).send_success_response()
        

class teacherviewservices:
    
    #TEACHER VIEW OWN INFO
    def teacher_view_own__info(teacher_id: int,db: Session,current_user: User):
        
        if current_user.role != "teacher" or current_user.id != teacher_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view the information"
            )
        
        teacher = db.query(User).filter(User.id == teacher_id, User.role == "teacher").first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )
        
        response_data = {
            "id": teacher.id,
            "username": teacher.username,
            "email": teacher.email,
            "class": teacher.class_name,
            "subject": teacher.subject_name,
        }
        return Response(
            status_code=200,
            message="Teacher details retrieved successfully",
            data=response_data
        ).send_success_response()

   
    #TEACHER VIEW OWN SALARY
    def teacher_view_own_salary( db: Session, current_user = User):
        
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Not authorized to view this salary")
        
        salary = db.query(User).filter(User.salary == current_user.salary).first()

        if current_user.salary is None:
            raise HTTPException(status_code=404, detail="Salary not set for this teacher")

        response_data = {
            "id": current_user.id,
            "username": current_user.username,
            "salary": current_user.salary,
        }
        return Response(
            status_code=200,
            message="Teacher salary details retrieved successfully",
            data= response_data 
        ).send_success_response()


    #TEACHER VIEW STUDENT INFO
    def teacher_view_student_info(student_id: int, current_user, db: Session):

        if current_user.role != "teacher":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher authorization required")
        
        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
        response_data = {
            "id": student.id,
            "username": student.username,
            "email": student.email,
            "class": student.class_name,
        }
        return Response(
            status_code=200,
            message="student details retrieved successfully",
            data= response_data 
        ).send_success_response()
        
class studentviewservices:
    
    #STUDENT VIEW OWN INFO
    def student_view_own__info(student_id: str,db: Session,current_user= User):
        
        print(f"Debug: current_user.id = {current_user.id}, student_id = {student_id}")
        
        if str(current_user.id) != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only view your own information"
            )
        
        student = db.query(User).filter(User.id == student_id, User.role == "student").first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        response_data = {
            "id": student.id,
            "username": student.username,
            "email": student.email,
            "class": student.class_name,
        }
        return Response(
            status_code=200,
            message="Student details retrieved successfully",
            data=response_data
        ).send_success_response()


