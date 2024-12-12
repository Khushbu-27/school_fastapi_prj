
from fastapi import APIRouter
from app.src.api.v1.users.views.admin_views.admin_views import admin_router 
from app.src.api.v1.users.views.admin_views.admin_service_views import admin_serv_router
from app.src.api.v1.users.views.user_views.user_views import user_router
from app.src.api.v1.users.views.user_views.teacher_views import teacher_serv_router
from app.src.api.v1.users.views.user_views.student_views import student_serv_router
from app.src.api.v1.exams.views.examviews import teacher_exam_router
from app.src.api.v1.marks.views.marksviews import teacher_marks_router ,student_marks_router
from app.src.api.v1.users.services.loginusers.facebooklogin import facebook_login_router
from app.src.api.v1.users.services.loginusers.googlelogin import google_login_router

router = APIRouter()

router.include_router(admin_router)
router.include_router(user_router)  
router.include_router(admin_serv_router)  
router.include_router(teacher_serv_router) 
router.include_router(student_serv_router)
router.include_router(teacher_exam_router)
router.include_router(teacher_marks_router)
router.include_router(student_marks_router)
router.include_router(facebook_login_router)
router.include_router(google_login_router)