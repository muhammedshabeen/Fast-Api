from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/create-blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/get-blog',response_model=List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog-detail/{id}', status_code=200)
def detail_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    return blog


@app.delete('/delete-blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog_to_delete = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_to_delete.first():
        return {
            "status": 0,
            "message": "Blog not found"
        }

    blog_to_delete.delete(synchronize_session=False)
    db.commit()
    return {
        "status": 1,
        "message": " Blog deleted"
    }


@app.put('/update-blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_to_update.first():
        return {
            "status": 0,
            "message": "Blog not found"
        }

    blog_to_update.update(request.dict())
    db.commit()
    return {
        "status": 1,
        "message": "Updated"
    }






@app.post('/create-user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user