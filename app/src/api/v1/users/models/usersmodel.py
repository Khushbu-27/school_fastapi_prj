
from sqlalchemy import BigInteger, Column, Integer, String , Date
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

    # marks = relationship("StudentMarks", back_populates="user"
    
    def format_phone_number(phone_number):
        
        if not phone_number.startswith('+91'):
            phone_number = '+91' + phone_number
        return phone_number