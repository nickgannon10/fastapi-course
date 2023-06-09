from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote, llm, doctor_patient
from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#place website url in origins eventually
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #maybe modify to only allow GET for security
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(llm.router)
app.include_router(doctor_patient.router)



@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}
