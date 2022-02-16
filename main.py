import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from recommendations import latest, getRecommendations

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputMovies(BaseModel):
    id: str
    tconst: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movies")
async def get_movies():
    start = time.time()
    result = latest()
    print(time.time() - start)
    if result:
        return json.dumps(result)
    else:
        raise HTTPException(404, "API error! Database is updating. Please try after some time..")


@app.post("/get-recommendations")
async def get_recommendations(movie_schema: InputMovies):
    result = getRecommendations(dict(movie_schema))
    if result:
        return json.dumps(result)
    else:
        raise HTTPException(404, "Data not found!")
