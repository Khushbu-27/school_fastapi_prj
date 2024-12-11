
    
from pydantic import BaseModel, Field

class Exam(BaseModel):
    
    class_name: int = Field(..., ge=0, le=12, description="Exam must be between 0 and 12.") 
    subject_name: str
    marks: int = Field(..., ge=0, le=100, description="Marks must be between 0 and 100.") 
    