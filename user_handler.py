from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

from src.config.config import settings
from src.data.entity.models import User, PlayerInGame, Match
from src.data.repo.project_repo import connect_db
from src.data.entity.schemas import UserSchema, PlayerInGameSchema

user_router = APIRouter(
    prefix=settings.api_pref
)


@user_router.get("/user/{user_id}")
async def get_user(user_id: int, database=Depends(connect_db)):
    print(user_id)
    user_list = database.query(User).filter(
        User.id == user_id).first()
    if user_list:
        return user_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No user with this id: {user_id} found')


@user_router.get("/users")
async def get_users(database=Depends(connect_db)):
    user_list = database.query(User).all()
    if user_list:
        return user_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No users found')


@user_router.get("/users/search")
async def get_user_by_login(login: str, database=Depends(connect_db)):
    user_list = database.query(User).filter(
        User.login == login).first()
    if user_list:
        return user_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No user with this login: {login} found')


@user_router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
        request: Request,
        response: Response,
        new_user: UserSchema,
        database=Depends(connect_db)):

    try:
        database.begin()
        new_user = User(**new_user.dict())
        database.add(new_user)
        database.commit()
        database.refresh(new_user)
    except Exception as e:
        database.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
    return {"status": "success", "user": new_user}


@user_router.post("/users/add_game", status_code=status.HTTP_201_CREATED)
async def add_game_to_user(
        request: Request,
        response: Response,
        new_user_in_game: PlayerInGameSchema,
        database=Depends(connect_db)):
    try:
        database.begin()
        new_user_in_game = PlayerInGame(**new_user_in_game.dict())
        database.add(new_user_in_game)
        database.commit()
        database.refresh(new_user_in_game)
    except Exception as e:
        database.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
    return {"status": "success", "user_in_game": new_user_in_game}


@user_router.get("/user/{user_id}/new_matches")
async def find_new_matches(user_id: int, database=Depends(connect_db)):
    temp = database.query(Match).filter(Match.user_1_id == user_id).all()
    print(temp)
    user_list = database.query(User).filter(User.id != user_id).filter(User.id.not_in(
        database.query(Match.user_2_id).filter(Match.user_1_id == user_id))).all()
    return user_list


@user_router.patch("/user/{user_id}/link")
async def change_pic_url_by_user_id(user_id: int, new_url: str, database=Depends(connect_db)):
    user_list = database.query(User).filter(
        User.id == user_id).first()
    if user_list:
        user_list.link = new_url
        database.commit()
        database.refresh(user_list)
        return {"status": "success", "user": user_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No user with this id: {user_id} found')


@user_router.patch("/user/{user_id}/name")
async def change_name_by_user_id(user_id: int, name: str, database=Depends(connect_db)):
    user_list = database.query(User).filter(
        User.id == user_id).first()
    if user_list:
        user_list.name = name
        database.commit()
        database.refresh(user_list)
        return {"status": "success", "user": user_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No user with this id: {user_id} found')


@user_router.patch("/user/{user_id}/gender")
async def change_gender_by_user_id(user_id: int, gender: str, database=Depends(connect_db)):
    user_list = database.query(User).filter(
        User.id == user_id).first()
    if user_list:
        user_list.gender = gender
        database.commit()
        database.refresh(user_list)
        return {"status": "success", "user": user_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No user with this id: {user_id} found')
