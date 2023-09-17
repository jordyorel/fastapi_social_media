from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Retrieve all posts (GET method)
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""
):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()

    posts = db.query(
        models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = []

    for post in posts:
        vote_count = db.query(func.count(models.Vote.post_id)).filter(
            models.Vote.post_id == post.id).scalar()
        post_dict = post.__dict__  # Convert SQLAlchemy model to dictionary
        post_dict['owner'] = {
            'id': post.owner.id,
            'email': post.owner.email,
            'created_at': post.owner.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        # Use 'post' field with the updated dictionary
        post_out = schemas.PostOut(post=post_dict, votes=vote_count)
        result.append(post_out)

    # print((result))
    return result

# Retrieve a specific post by ID (GET method)
@router.get("/{post_id}", response_model=schemas.PostOut)
def get_one_post(post_id: int, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the ID {post_id} was not found"
        )

    vote_count = db.query(func.count(models.Vote.post_id)).filter(models.Vote.post_id == post_id).scalar()
    # Create a dictionary for the "post" field
    post_dict = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at,  # Include actual created_at data
        "owner_id": post.owner_id,  # Include actual owner_id data
        "owner": {
            "id": post.owner.id,  # Include actual owner data
            "email": post.owner.email,  # Include actual owner email data
            'created_at': post.owner.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    reponse_model = schemas.PostOut(post=post_dict, votes=vote_count)
    return reponse_model


# Create a new post (POST method)
@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(
        get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email) # not printing the user email (error)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Delete a post by ID (DELETE method)
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    # Check if the post with the given ID exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} was not found"
        )

    # Check if the post belongs to the current user
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )

    db.delete(post)
    db.commit()
    return None


# Update a post by ID (PUT method)
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    # Check if the post with the given ID exists
    existing_post = db.query(
        models.Post).filter(
        models.Post.id == post_id).first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with the ID {post_id} was not found"
        )

    # Check if the post belongs to the current user
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post"
        )

    # Update the post data
    for key, value in updated_post.dict().items():
        setattr(existing_post, key, value)

    # Commit the changes to the database
    db.commit()
    db.refresh(existing_post)

    return existing_post

