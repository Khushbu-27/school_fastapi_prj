
def indiviual_serial(exam) -> dict:
    return {
        
        "id": str(exam["_id"]),
        "class_name": exam["class_name"],
        "subject_name": exam["subject_name"],
        "marks": exam["marks"]
    }
    
def list_serial(exams) -> list:
    return [indiviual_serial(exam) for exam in exams]