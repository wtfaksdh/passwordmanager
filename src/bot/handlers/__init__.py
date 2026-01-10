"""Handlers package initialization"""
from src.bot.handlers.auth import router as auth_router, user_sessions as auth_sessions
from src.bot.handlers.password import router as password_router, user_sessions as password_sessions

# Merge sessions dictionaries to keep them in sync
user_sessions = auth_sessions

# Main router that includes all handlers
main_router = None


def init_routers():
    """Initialize all routers"""
    from aiogram import Router
    
    global main_router
    main_router = Router()
    main_router.include_router(auth_router)
    main_router.include_router(password_router)
    
    return main_router


__all__ = ["init_routers", "user_sessions"]
