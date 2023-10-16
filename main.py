from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(bind=engine)


class post_base(BaseModel):
    title: str
    content: str
    user_id: int


class user_base(BaseModel):
    username: str
    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   

db_dependency = Annotated[Session, Depends(get_db)]


# get all post
@app.get("/posts", status_code=status.HTTP_200_OK, tags=["Post"])
async def get_all_post(db: db_dependency):
    get_post = db.query(model.Post).all()
    return get_post


# post store
@app.post("/posts/", status_code=status.HTTP_201_CREATED, tags=["Post"])
async def created_post(post: post_base, db: db_dependency):
    db_post = model.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# post search by id
@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK, tags=['Post'])
async def read_post(post_id: int, db: db_dependency):
    post = db.query(model.Post).filter(model.Post.id == post_id).first()
    if post is None:
        return HTTPException(status_code=404, detail="Post not found!")
    return post


# post delete by id
@app.get("/posts/{delete_id}", status_code=status.HTTP_200_OK, tags=["Post"])
async def delete_post(delete_id: int, db: db_dependency):
    delete_post = db.query(model.Post).filter(model.Post.id == delete_id).first()
    if delete_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(delete_post)
    db.commit()
    return HTTPException(status_code=200, detail="Post has been deleted successfully!")


#  user store
@app.get("/users/", status_code=status.HTTP_200_OK, tags=["User"])
async def get_user(db: db_dependency):
    all_user = db.query(model.User).all()
    return HTTPException(status_code=200, detail=all_user)


#  user store
@app.post("/users/", status_code=status.HTTP_201_CREATED, tags=["User"])
async def create_user(user: user_base, db: db_dependency):
    db_user = model.User(**user.dict())
    db.add(db_user) 
    db.commit()
    db.refresh(db_user)
    return db_user


# user search by id
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["User"])
async def read_user(user_id: int, db: db_dependency):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail="User not found!")
    return user


# user delete by id
@app.get("/users/{delete_user}", status_code=status.HTTP_200_OK, tags=["User"])
async def delete_user(delete_user: int, db: db_dependency):
    user_delete = db.query(model.User).filter(model.User.id == delete_user).first()
    if user_delete is None:
        return HTTPException(status_code=404, detail="User not foundsss!")
    db.delete(user_delete)
    db.commit()
    return HTTPException(status_code=200, detail="User has been deleted successfully!")