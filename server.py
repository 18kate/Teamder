from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.config import settings
from src.service.handlers.user_handler import user_router
from src.service.handlers.game_handler import game_router
from src.service.handlers.match_handler import match_router
# from src.service.handlers.shop_handler import shop_router
# from src.service.handlers.product_in_shop_handler import product_in_shop_router
# from src.service.handlers.cart_handler import cart_router
# from src.service.handlers.product_in_cart_handler import product_in_cart_router
from src.data.repo.project_repo import create_db


def get_application() -> FastAPI:
    application = FastAPI(title=settings.title)

    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(user_router)
    application.include_router(game_router)
    application.include_router(match_router)
    # application.include_router(shop_router)
    # application.include_router(product_in_shop_router)
    # application.include_router(cart_router)
    # application.include_router(product_in_cart_router)
    return application


create_db()
app = get_application()
