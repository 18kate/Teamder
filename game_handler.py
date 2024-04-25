from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy import func

from src.config.config import settings
from src.data.entity.models import Game
from src.data.repo.project_repo import connect_db
from src.data.entity.schemas import GameSchema

game_router = APIRouter(
    prefix=settings.api_pref
)


@game_router.get("/game/{game_id}")
async def get_game(game_id: int, database=Depends(connect_db)):
    game_list = database.query(Game).filter(
        Game.id == game_id).first()
    if game_list:
        return game_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No game with this id: {game_id} found')


@game_router.get("/games")
async def get_games(database=Depends(connect_db)):
    game_list = database.query(Game).order_by(Game.name).all()
    if game_list:
        return game_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No games found')


@game_router.get("/games/search")
async def get_game_by_name(name: str, database=Depends(connect_db)):
    user_list = database.query(Game).filter(
        func.lower(Game.name).contains(name.lower())).order_by(Game.name).all()

    if user_list:
        return user_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No game with this name: {name} found')


@game_router.post("/games", status_code=status.HTTP_201_CREATED)
async def create_game(
        request: Request,
        response: Response,
        new_game: GameSchema,
        database=Depends(connect_db)):

    try:
        database.begin()
        new_game = Game(**new_game.dict())
        database.add(new_game)
        database.commit()
        database.refresh(new_game)
    except Exception as e:
        database.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
    return {"status": "success", "game": new_game}


@game_router.patch("/game/{game_id}/picture_url")
async def change_pic_url_by_game_id(game_id: int, new_pic_url: str, database=Depends(connect_db)):
    game_list = database.query(Game).filter(
        Game.id == game_id).first()
    if game_list:
        game_list.picture_url = new_pic_url
        database.commit()
        database.refresh(game_list)
        return {"status": "success", "game": game_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No game with this id: {game_id} found')


@game_router.patch("/game/{game_id}/has_rank")
async def change_has_rank_by_game_id(game_id: int, new_has_rank: bool, database=Depends(connect_db)):
    game_list = database.query(Game).filter(
        Game.id == game_id).first()
    if game_list:
        game_list.has_rank = new_has_rank
        database.commit()
        database.refresh(game_list)
        return {"status": "success", "game": game_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No game with this id: {game_id} found')
