from fastapi import status, Depends, Response, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..exceptions import PostNotExistException
from ..models import Post, User, Vote
from ..schemas import PostCreate, PostResponse, PostOut
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str | None = ""):
    posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id,
                                                                           isouter=True).group_by(Post.id).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: PostCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    new_post = Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise PostNotExistException(post_id=post_id)

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_post = db.query(Post).filter(Post.id == post_id).first()
    if deleted_post is None:
        raise PostNotExistException(post_id=post_id)
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    updated_post_query = db.query(Post).filter(Post.id == post_id)
    if updated_post_query.first() is None:
        raise PostNotExistException(post_id=post_id)
    if updated_post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    updated_post_query.update(post.dict())
    db.commit()

    updated_post = updated_post_query.first()
    return updated_post
