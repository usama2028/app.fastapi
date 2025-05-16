from fastapi import APIRouter,status,Response,HTTPException,Depends
from sqlmodel import select
from app import schemas,database,oauth2,models

router=APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,session:database.SessionDep,current_user:models.Users=Depends(oauth2.get_current_user)):
    post=session.get(models.Posts,vote.post_id)
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id of {vote.post_id} does not exists..")
    vote_query=session.exec(select(models.Vote).where(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id))
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message":"the vote created sucessfully"}
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The vote does not exists.")
        session.delete(found_vote)
        session.commit()

        return {"message":"vote deleted sucessfully.."}
