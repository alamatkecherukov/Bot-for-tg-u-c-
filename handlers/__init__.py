from aiogram import Router
from . import user

def setup_routers() -> Router:
    router = Router()
    router.include_router(user.router)
    return router
