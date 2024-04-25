from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

from src.config.config import settings
from src.data.entity.models import Match
from src.data.repo.project_repo import connect_db
from src.data.entity.schemas import MatchSchema

match_router = APIRouter(
    prefix=settings.api_pref
)


@match_router.post("/matches", status_code=status.HTTP_201_CREATED)
async def create_match(
        request: Request,
        response: Response,
        new_match: MatchSchema,
        database=Depends(connect_db)):
    print(new_match)
    try:
        database.begin()
        new_match = Match(**new_match.dict())
        database.add(new_match)
        database.commit()
        database.refresh(new_match)
    except Exception as e:
        database.rollback()
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": e,
            "error_details": e.orig.args if hasattr(e, 'orig') else f"{e}"
        }
    return {"status": "success", "match": new_match}


@match_router.patch("/match/patch")
async def change_has_rank_by_game_id(user_1_id: int, user_2_id: int, user_1_has_liked: bool = None, user_2_has_liked: bool = None, database=Depends(connect_db)):
    match_list = database.query(Match).filter(
        Match.user_1_id == user_1_id).filter(Match.user_2_id == user_2_id).first()
    if match_list:
        if user_1_has_liked:
            match_list.user_1_has_liked = user_1_has_liked
        if user_2_has_liked:
            match_list.user_2_has_liked = user_2_has_liked
        database.commit()
        database.refresh(match_list)
        return {"status": "success", "game": match_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No match with this ids: {(user_1_id, user_2_id)} found')


@match_router.get("/match/get_all")
async def get_all_matches(database=Depends(connect_db)):
    match_list = database.query(Match).all()
    if match_list:
        return {"status": "success", "matches": match_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No matches found')


@match_router.get("/match/find_all_unanswered")
async def get_all_unanswered(user_id: int, database=Depends(connect_db)):
    match_list = database.query(Match).filter(
        Match.user_2_id == user_id).filter(Match.user_2_has_liked == None).all()
    if match_list:
        return {"status": "success", "matches": match_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'No matches found')
