
import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.services.crud.createusers import adminservices
from app.src.api.v1.users.services.crud.deleteusers import userdeleteservices
from app.src.api.v1.users.services.crud.updateusers import adminupdateservices
from app.src.api.v1.users.services.crud.viewusers import adminviewservices
from app.src.api.v1.users.services.loginusers.login import loginservices
from app.src.api.v1.users.schemas.userschemas import AdminCreate, StudentCreate, TeacherCreate, TeacherSalary, UserUpdate
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_admin, authorize_user


admin_router = APIRouter()
admin_serv_router = APIRouter()


@admin_router.post("/admin/register")
def admin_register(admin: AdminCreate, db: Session = Depends(get_db)):
    return loginservices.admin_register(admin,db)

@admin_serv_router.post("/admin/add_student", tags=["admin"])
def create_student(student: StudentCreate, db: Session = Depends(get_db), token: str = Depends(authorize_admin)):
        return adminservices.create_student(student,db,token)
    
@admin_serv_router.post("/admin/add_teacher", tags=["admin"])
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db), token: str = Depends(authorize_admin)):
        return adminservices.create_teacher(teacher,db,token)
        
@admin_serv_router.post("/admin/add_teacher_salary/{teacher_id}", tags=["admin"])
def add_teacher_salary(teacher_id: int, salary: TeacherSalary, db: Session = Depends(get_db), current_user = Depends(authorize_admin) ):
        return adminservices.add_teacher_salary(teacher_id,salary,db,current_user)
    
@admin_serv_router.get("/admin/{admin_id}", tags=["admin"])
def admin_view_own_info(admin_id: int, token: dict = Depends(authorize_admin), db: Session = Depends(get_db), current_user = Depends(authorize_admin)):
        return adminviewservices.admin_view_own_info(admin_id, token , db)
    
@admin_serv_router.get("/admin/view_student/{student_id}", tags=["admin"])
def admin_view_student_info(student_id: int, token: str = Depends(authorize_admin), db: Session = Depends(get_db)):
        return adminviewservices.admin_view_student_info(student_id,token,db)

@admin_serv_router.get("/admin/view_teacher/{teacher_id}", tags=["admin"])
def admin_view_teacher_info(teacher_id: int, token: str = Depends(authorize_admin), db: Session = Depends(get_db)):
        return adminviewservices.admin_view_teacher_info(teacher_id,token,db)
    
@admin_serv_router.get("/admin/view_teacher_salary/{teacher_id}", tags=["admin"])
def admin_view_teacher_salary(teacher_id: int, db: Session = Depends(get_db), current_user = Depends(authorize_admin)):
        return adminviewservices.admin_view_teacher_salary(teacher_id,db,current_user)
    
@admin_serv_router.put("/admin/update/{admin_id}",tags=["admin"])
def admin_update_own_info(update_data: UserUpdate, current_user = Depends(authorize_admin), db: Session = Depends(get_db)):
        return adminupdateservices.admin_update_own_info(update_data,current_user,db)

   
@admin_serv_router.put("/admin/update_salary/{teacher_id}", tags=["admin"])
def admin_update_teacher_salary(teacher_id: int,salary: TeacherSalary, db: Session = Depends(get_db), current_user: User = Depends(authorize_admin)):  
        return adminupdateservices.admin_update_teacher_salary(teacher_id,db,current_user,salary)
    
@admin_serv_router.delete("/admin/delete_user/{user_id}", tags=["admin"] )
def admin_delete_user(user_id: int,admin_id: int = Query(...) ,current_user=Depends(authorize_user), db: Session = Depends(get_db)):
        return userdeleteservices.admin_delete_user(user_id,current_user,db, admin_id)



