from fastapi import FastAPI

from app.api import files

app = FastAPI()

app.include_router(files.router, prefix='/files', tags=['files'])
