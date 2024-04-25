from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    login = Column(String)
    email = Column(String)
    password = Column(String)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    link = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=True)
    # created_at = Column(DateTime)
    # updated_at = Column(DateTime)


class Pictures(Base):
    __tablename__ = 'pictures'
    __table_args__ = {
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    order = Column(Integer)
    picture_url = Column(String)


class Game(Base):
    __tablename__ = 'game'
    __table_args__ = {
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)
    picture_url = Column(String, nullable=True)
    has_rank = Column(Boolean)


class Rank(Base):
    __tablename__ = 'rank'
    __table_args__ = {
        'extend_existing': True
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey(Game.id))
    name = Column(String)
    picture_url = Column(String)
    order = Column(Integer)


class PlayerInGame(Base):
    __tablename__ = 'playeringame'
    __table_args__ = {
        'extend_existing': True
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey(Game.id))
    user_id = Column(Integer, ForeignKey(User.id))
    has_played = Column(Boolean)
    hours_played = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)


class PlayerRank(Base):
    __tablename__ = 'playerrank'
    __table_args__ = {
        'extend_existing': True
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey(Game.id))
    user_id = Column(Integer, ForeignKey(User.id))
    rank_id = Column(Integer, ForeignKey(Rank.id))


class Match(Base):
    __tablename__ = 'match'
    __table_args__ = {
        'extend_existing': True
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_1_id = Column(Integer, ForeignKey(User.id))
    user_2_id = Column(Integer, ForeignKey(User.id))
    user_1_has_liked = Column(Boolean, nullable=True)
    user_2_has_liked = Column(Boolean, nullable=True)

    def __repr__(self):
        return f'{self.user_1_id}-{self.user_2_id}'
