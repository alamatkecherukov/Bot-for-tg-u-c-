from aiogram import Router
from . import user, teacher

def setup_routers() -> Router:
    router = Router()
    router.include_router(user.router)
    router.include_router(teacher.router)
    return router
