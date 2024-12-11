
from fastapi import APIRouter, Depends
from requests import Session
from app.database.database import get_db
from app.src.api.v1.users.schemas.userschemas import StudentResponse, UserUpdate
from app.src.api.v1.users.services.crud.updateusers import studentupdateservices
from app.src.api.v1.users.services.crud.viewusers import studentviewservices
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user


student_serv_router = APIRouter()
    
@student_serv_router.get("/student/{student_id}", tags=["student"])
def student_view_own_info(student_id: str,db: Session = Depends(get_db),current_user=Depends(authorize_user)):
    return studentviewservices.student_view_own__info(student_id,db,current_user)
    
@student_serv_router.put("/student/update/{student_id}", response_model=StudentResponse ,tags=["student"])
def student_update_own_info(update_data: UserUpdate, current_user = Depends(authorize_user), db: Session = Depends(get_db)):
    return studentupdateservices.student_update_own_info(update_data,current_user,db)