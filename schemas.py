from datetime import datetime
from typing import TypeVar, List
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    login: str
    email: str
    password: str
    location: str = None
    description: str = None
    birth_date: datetime = None
    gender: str = None
    link: str = None
    is_admin: bool = None
    # created_at: datetime
    # updated_at: datetime


class GameSchema(BaseModel):
    name: str
    has_rank: bool
    description: str = None
    picture_url: str = None


class PlayerInGameSchema(BaseModel):
    game_id: int
    user_id: int
    has_played: bool
    rating: float = None
    hours_played: bool = None


class MatchSchema(BaseModel):
    user_1_id: int
    user_2_id: int
    user_1_has_liked: bool = None
    user_2_has_liked: bool = None
