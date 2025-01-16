from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from actual_project.main import solver_race_to_description, solver_description_to_cat_breed, compare_breeds

app = FastAPI()

# Request and response models
class BreedRequest(BaseModel):
    breed: str
class BreedComparisonRequest(BaseModel):
    breed1: str
    breed2: str

class DescriptionRequest(BaseModel):
    description: str
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:54013",
    "http://127.0.0.1:54013/",
    "http://localhost:54648"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/generate")
async def generate_description(request: BreedRequest):
    # Placeholder logic - replace with your code
    breed = request.breed
    description = solver_race_to_description(breed)
    return {"breed": breed, "description": description}

@app.post("/api/identify")
async def identify_breed(request: DescriptionRequest):
    # Placeholder logic - replace with your code
    description = request.description
    breed = solver_description_to_cat_breed(description)
    return {"description": description, "breed": breed}

# Run the application: uvicorn cat_api:app --reload --host 0.0.0.0 --port 8000
@app.post("/api/compare-breeds")
async def compare_breeds_req(request: BreedComparisonRequest):
    breed1 = request.breed1
    breed2 = request.breed2
    fp=open('debug.txt','w')
    fp.write(breed1)
    fp.write(breed2)
    fp.close()
    description = compare_breeds(breed1, breed2)
    return {"description": description}