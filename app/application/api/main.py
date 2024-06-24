from fastapi import FastAPI
from application.api.users.handlers import router as user_router
from application.api.auth.handlers import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="simple todo list",
        docs_url="/api/docs",
        description="simple todo list with email notification + DDD",
        debug=True
    )
    app.include_router(router=user_router, prefix='/users')
    app.include_router(router=auth_router, prefix='/auth')

    return app
