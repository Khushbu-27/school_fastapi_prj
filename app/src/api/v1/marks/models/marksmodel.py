
from sqlalchemy import Column, ForeignKey, Integer, String
from app.database.database import Base
from sqlalchemy.orm import relationship 


class StudentMarks(Base):
    
    __tablename__ = "student_marks"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)  
    class_name = Column(Integer, nullable=False)    
    subject_name = Column(String, nullable=False) 
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)   
    student_marks = Column(Integer, nullable=False) 
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # user = relationship("User", back_populates="marks")
    exam = relationship("Exam", back_populates="student_marks")
    #     "Exam",
    #     primaryjoin="StudentMarks.exam_id == remote(Exam.id)",
    #     back_populates="marks_received",
    #     viewonly=True,
    # )
    
    