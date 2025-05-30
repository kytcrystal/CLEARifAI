from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router

import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI()
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
