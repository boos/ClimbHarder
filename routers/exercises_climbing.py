from fastapi import APIRouter, Depends, status

from misc.security import oauth2_scheme


router = APIRouter(dependencies=[Depends(oauth2_scheme)])


@router.get("/exercises/climbing/grade/", status_code=status.HTTP_200_OK)
async def create_user(user: UserCreation):
    pass
