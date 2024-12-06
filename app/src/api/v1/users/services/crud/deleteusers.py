
from fastapi import HTTPException, Query
from sqlalchemy.orm import Session
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.services.user_authentication.user_auth import authorize_user
from app.src.api.v1.utils.response_utils import Response


class userdeleteservices:
    
    #ADMIN DELETE USERS
    def admin_delete_user(user_id: int,db: Session, current_user: User,admin_id: int ):
        
        admin = db.query(User).filter(User.id == admin_id, User.role == "admin").first()

        if not admin:
            raise HTTPException(status_code=403, details= 'Only admin can delete users')
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(user)
        db.commit()
        response_data = {
            "id": user.id,
            "username": user.username,
            "email":user.email
        }
        return Response(
            status_code=200,
            message="User delete successfully",
            data= response_data 
        ).send_success_response()   