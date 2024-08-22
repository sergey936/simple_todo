from fastapi import FastAPI
from punq import Container

from application.api.lifespan import start, stop
from application.api.users.handlers import router as user_router
from application.api.auth.handlers import router as auth_router
from application.api.tasks.handlers import router as task_router
from logic.init import init_container


async def lifespan(app: FastAPI):
    await start()
    yield
    await stop()


def create_app() -> FastAPI:
    container = init_container()

    app = FastAPI(
        title="simple todo list",
        docs_url="/api/docs",
        description="simple todo list with email notification + DDD",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(router=user_router, prefix='/users')
    app.include_router(router=auth_router, prefix='/auth')
    app.include_router(router=task_router, prefix='/tasks')

    return app
