from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movies")
async def get_movies():
    result = latest()
    if result:
        return result
    else:
        raise HTTPException(404, "API error! Data not found.")


@app.get("/get-recommendations")
async def get_recommendations(movie_name: str):
    result = getRecommendations(movie_name)
    if result:
        return result
    else:
        raise HTTPException(404, "Data not found!")
