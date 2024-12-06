
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.schemas.userschemas import StudentResponse, TeacherResponse, UserUpdate
from app.src.api.v1.users.services.crud.updateusers import studentupdateservices, teacherupdateservices
from app.src.api.v1.users.services.crud.viewusers import studentviewservices, teacherviewservices
from app.src.api.v1.users.services.forgotpass.forgotpass import forgotpassservices
from app.src.api.v1.users.services.loginusers.login import loginservices
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user

teacher_serv_router = APIRouter()
student_serv_router = APIRouter()
user_router = APIRouter()

@user_router.post('/login')
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return loginservices.login(db,form_data.username, form_data.password )

@user_router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    return forgotpassservices.forgot_password(email,db)
    
@user_router.post("/reset-password")
def reset_password(user_id: int, email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    return forgotpassservices.reset_password(user_id,email,otp,new_password,db)

@teacher_serv_router.get("/teacher/{teacher_id}",tags=["teacher"])
def teacher_view_own__info(teacher_id: int,db: Session = Depends(get_db),current_user: User=Depends(authorize_user)):
    return teacherviewservices.teacher_view_own__info(teacher_id,db,current_user)
   
@teacher_serv_router.get("/teacher/view_salary/{teacher_id}", tags=["teacher"])
def teacher_view_own_salary( db: Session = Depends(get_db), current_user = Depends(authorize_user)):
    return teacherviewservices.teacher_view_own_salary(db,current_user)
        
@teacher_serv_router.get("/teacher/view_student/{student_id}", tags=["teacher"])
def teacher_view_student_info(student_id: int, current_user = Depends(authorize_user), db: Session = Depends(get_db)):
    return teacherviewservices.teacher_view_student_info(student_id,current_user,db)
    
@teacher_serv_router.put("/teacher/update/{teacher_id}", response_model=TeacherResponse,  tags=["teacher"])
def teacher_update_own_info(update_data: UserUpdate, current_user = Depends(authorize_user), db: Session = Depends(get_db)):
    return teacherupdateservices.teacher_update_own_info(update_data,current_user,db)
    
    
@student_serv_router.get("/student/{student_id}", tags=["student"])
def student_view_own_info(student_id: str,db: Session = Depends(get_db),current_user=Depends(authorize_user)):
    return studentviewservices.student_view_own__info(student_id,db,current_user)
    
@student_serv_router.put("/student/update/{student_id}", response_model=StudentResponse ,tags=["student"])
def student_update_own_info(update_data: UserUpdate, current_user = Depends(authorize_user), db: Session = Depends(get_db)):
    return studentupdateservices.student_update_own_info(update_data,current_user,db)
