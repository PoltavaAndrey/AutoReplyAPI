from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import DeleteTables, CreateTables
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DeleteTables()
    print("База очищена!")
    await CreateTables()
    print("База готова к работе!")
    yield
    print("Выключение!")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
