
from fastapi import APIRouter, Depends
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.schemas.userschemas import TeacherResponse, UserUpdate
from app.src.api.v1.users.services.crud.updateusers import teacherupdateservices
from app.src.api.v1.users.services.crud.viewusers import teacherviewservices
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user


teacher_serv_router = APIRouter()

@teacher_serv_router.get("/teacher/{teacher_id}",tags=["teacher"])
def teacher_view_own__info(teacher_id: int,db: Session = Depends(get_db),current_user: User=Depends(authorize_user)):
    return teacherviewservices.teacher_view_own__info(teacher_id,db,current_user)
   
@teacher_serv_router.get("/teacher/view_salary/{teacher_id}", tags=["teacher"])
def teacher_view_own_salary( db: Session = Depends(get_db), current_user = Depends(authorize_user)):
    return teacherviewservices.teacher_view_own_salary(db,current_user)
        
@teacher_serv_router.get("/teacher/view_student/{student_id}", tags=["teacher"])
def teacher_view_student_info(student_id: int, db: Session = Depends(get_db), current_user = Depends(authorize_user)):
    return teacherviewservices.teacher_view_student_info(db,student_id,current_user)
    
@teacher_serv_router.put("/teacher/update/{teacher_id}", response_model=TeacherResponse,  tags=["teacher"])
def teacher_update_own_info(update_data: UserUpdate, current_user = Depends(authorize_user), db: Session = Depends(get_db)):
    return teacherupdateservices.teacher_update_own_info(update_data,current_user,db)
    