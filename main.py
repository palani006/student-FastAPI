from router import auth, students,ai
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
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
   allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "Student API is running"}