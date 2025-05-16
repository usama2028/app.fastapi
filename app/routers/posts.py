from fastapi import HTTPException,Response,status,APIRouter,Depends
from app import schemas,models
from app.database import SessionDep
from sqlmodel import select,func
from sqlalchemy.orm import joinedload
from app import oauth2
from typing import Optional,List

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



@router.get("/", response_model=List[schemas.PostOut])
def get_posts(session: SessionDep,
              current_user: models.Users = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    print(current_user)

    statement = (
        select(models.Posts, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Posts.id == models.Vote.post_id, isouter=True)
        .group_by(models.Posts.id)
        .filter(models.Posts.title.contains(search)) # type: ignore
        .limit(limit)
        .offset(skip)
    )

    results = session.exec(statement).all()

    response = [{"Post": post, "votes": votes} for post, votes in results]

    return response

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate,
                session:SessionDep,
                current_user:models.Users = Depends(oauth2.get_current_user)):
    assert current_user.id is not None
    # new_post=models.Posts(title=post.title,content=post.content,publish=post.publish)
    new_post=models.Posts(user_id=current_user.id,**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id,session:SessionDep,current_user:models.Users=Depends(oauth2.get_current_user)):
    statement=select(models.Posts,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Posts.id==models.Vote.post_id,isouter=True).where(models.Posts.id==id).group_by(models.Posts.id)
    post=session.exec(statement).first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with {id} does not exist..")
    post,votes=post

    return {"Post":post,"votes":votes}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(session:SessionDep,id:int,
                current_user:models.Users=Depends(oauth2.get_current_user)):

    deleted_post=session.get(models.Posts,id)
    if deleted_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with the id {id} does not exist..")
    if deleted_post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="NOT AUTHORIZED TO PERFORM CERTAIN ACTIONS..")

    session.delete(deleted_post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(post:schemas.PostCreate,session:SessionDep,
                id:int,
                current_user:models.Users=Depends(oauth2.get_current_user)):

    updated_post=session.get(models.Posts,id)
    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with the id {id} does not exist..")
    if updated_post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=
                            "NOT AUTHORIZED TO PERFORM CERTAIN ACTIONS..")
    updated_post.title=(post.title)
    updated_post.content=(post.content)
    updated_post.publish=(post.publish)
    
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return updated_post
