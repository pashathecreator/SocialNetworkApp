from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..exceptions import UserNotExistException
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotExistException(user_id)

    return user
