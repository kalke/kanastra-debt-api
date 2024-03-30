from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import files, process

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(files.router, prefix='/files', tags=['files'])
app.include_router(process.router, prefix='/process', tags=['process'])
