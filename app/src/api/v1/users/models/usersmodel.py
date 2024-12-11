
from sqlalchemy import BigInteger, Column, Integer, String , Date
from sqlalchemy.orm import relationship
from app.database.database import Base


class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number = Column(BigInteger ,nullable=True)   
    email = Column(String, unique=True)
    role = Column(String) 
    salary = Column(BigInteger, nullable=True)  
    class_name = Column(Integer, nullable=True)  
    subject_name = Column(String, nullable=True)
    attendance = Column(Integer, default=0)
    last_login_date = Column(Date, nullable=True)
    
    def set_salary(self, salary):
        if not isinstance(salary, int) or salary < 0:
            raise ValueError("Salary must be a positive integer")
        self.salary = salary

    marks = relationship("StudentMarks", back_populates="user")
    
    def format_phone_number(phone_number):
        
        if not phone_number.startswith('+1'):
            phone_number = '+1' + phone_number
        return phone_number

    
    # @admin_serv_router.post("/admin/add_student", tags=["admin"])
    # def create_student(student: StudentCreate, db: Session = Depends(get_db), token: str = Depends(auth.authorize_admin)):
    #     return adminservices.create_student(student,db,token)
    
    # @admin_serv_router.post("/admin/add_teacher", tags=["admin"])
    # def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db), token: str = Depends(auth.authorize_admin)):
    #     return adminservices.create_teacher(teacher,db,token)
        
    # @admin_serv_router.post("/admin/add_teacher_salary/{teacher_id}", tags=["admin"])
    # def add_teacher_salary(teacher_id: int, salary: TeacherSalary, db: Session = Depends(get_db), current_user = Depends(auth.authorize_admin) ):
    #     return adminservices.add_teacher_salary(teacher_id,salary,db,current_user)
    
    # @admin_serv_router.get("/admin/{admin_id}", tags=["admin"])
    # def admin_view_own_info(admin_id: int, token: dict = Depends(auth.authorize_admin), db: Session = Depends(get_db), current_user = Depends(auth.authorize_admin)):
    #     return adminviewservices.admin_view_own_info(admin_id, token , db,current_user)
    
    # @admin_serv_router.get("/admin/view_student/{student_id}", tags=["admin"])
    # def admin_view_student_info(student_id: int, token: str = Depends(auth.authorize_admin), db: Session = Depends(get_db)):
    #     return adminviewservices.admin_view_student_info(student_id,token,db)

    # @admin_serv_router.get("/admin/view_teacher/{teacher_id}", tags=["admin"])
    # def admin_view_teacher_info(teacher_id: int, token: str = Depends(auth.authorize_admin), db: Session = Depends(get_db)):
    #     return adminviewservices.admin_view_teacher_info(teacher_id,token,db)
    
    # @admin_serv_router.get("/admin/view_teacher_salary/{teacher_id}", tags=["admin"])
    # def admin_view_teacher_salary(teacher_id: int, db: Session = Depends(get_db), current_user = Depends(auth.authorize_admin)):
    #     return adminviewservices.admin_view_teacher_salary(teacher_id,db,current_user)
    
    # @admin_serv_router.put("/admin/update/{admin_id}",tags=["admin"])
    # def admin_update_own_info(update_data: UserUpdate, current_user = Depends(auth.authorize_admin), db: Session = Depends(get_db)):
    #     return adminupdateservices.admin_update_own_info(update_data,current_user,db)
    
    # @admin_serv_router.put("/admin/update_salary/{teacher_id}", tags=["admin"])
    # def admin_update_teacher_salary(teacher_id: int,salary: TeacherSalary, db: Session = Depends(get_db), current_user = Depends(auth.authorize_admin)):
    #     return adminupdateservices.admin_update_teacher_salary(teacher_id,db,current_user)
    
    # @admin_serv_router.delete("/admin/delete_user/{user_id}", tags=["admin"] )
    # def admin_delete_user(user_id: int, current_user=Depends(auth.authorize_user), db: Session = Depends(get_db)):
    #     return userdeleteservices.admin_delete_user(user_id,current_user,db)
    
    
    # @teacher_serv_router.get("/teacher/{teacher_id}",tags=["teacher"])
    # def teacher_view_own__info(teacher_id: int,db: Session = Depends(get_db),current_user=Depends(auth.authorize_user)):
    #     return teacherviewservices.teacher_view_own__info(teacher_id,db,current_user)
   
    # @teacher_serv_router.get("/teacher/view_salary/{teacher_id}", tags=["teacher"])
    # def teacher_view_own_salary( db: Session = Depends(get_db), current_user = Depends(auth.authorize_user)):
    #     return teacherviewservices.teacher_view_own_salary(db,current_user)
        
    # @teacher_serv_router.get("/teacher/view_student/{student_id}", tags=["teacher"])
    # def teacher_view_student_info(student_id: int, current_user = Depends(auth.authorize_user), db: Session = Depends(get_db)):
    #     return teacherviewservices.teacher_view_student_info(student_id,current_user,db)
    
    # @teacher_serv_router.put("/teacher/update/{teacher_id}", response_model=TeacherResponse,  tags=["teacher"])
    # def teacher_update_own_info(update_data: UserUpdate, current_user = Depends(auth.authorize_user), db: Session = Depends(get_db)):
    #     return teacherupdateservices.teacher_update_own_info(update_data,current_user,db)
    
    
    # @student_serv_router.get("/student/{student_id}", tags=["student"])
    # def student_view_own_info(student_id: str,db: Session = Depends(get_db),current_user=Depends(auth.authorize_user)):
    #     return studentviewservices.student_view_own__info(student_id,db,current_user)
    
    # @student_serv_router.put("/student/update/{student_id}", response_model=StudentResponse ,tags=["student"])
    # def student_update_own_info(update_data: UserUpdate, current_user = Depends(auth.authorize_user), db: Session = Depends(get_db)):
    #     return studentupdateservices.student_update_own_info(update_data,current_user,db)
