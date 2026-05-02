import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from router import auth, students
import models.user     
import models.student  
from dotenv import load_dotenv
load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API", version="1.0.0")

FRONTEND_URL=os.getenv("FRONTEND_URL", "http://localhost:5173")
print(FRONTEND_URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/students", tags=["Students"])

@app.get("/")
def root():
    return {"message": "Student API is running"}