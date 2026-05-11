import os
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from google import genai
from google.genai import types
from dotenv import load_dotenv
from dependencies import get_current_user
router=APIRouter(prefix="/ai",tags=["AI"])
load_dotenv()

# Change "GENAI_API_KEY" to "GEMINI_API_KEY"
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")
client = genai.Client(api_key=api_key)
MODEL_NAME="gemini-3.1-flash-lite"
GENERATION_CONFIG=types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=512,
)
SYSTEM_CONTENT="""You are an AI assistant integrated into 
a Student Management System web application. Your role is 
to help users with academic, administrative, and programming-related
tasks in a clear and professional manner. You should explain Python 
programming concepts including syntax, functions, object-oriented programming
(OOP), file handling, APIs, and projects using simple language suitable for beginners.
Help students learn programming step-by-step and provide examples or sample code whenever needed.
Always keep responses well-formatted, easy to understand, and helpful. Ask for clarification if 
the request is unclear, avoid harmful or unrelated content, and ensure that sensitive student information 
remains private and secure."""

class AskRequest(BaseModel):
    question:str=Field(min_length=2,max_length=1000)
class AskResponse(BaseModel):
    answer:str
@router.post("/ask",response_model=AskResponse)
def ASK_AI(
    request:AskRequest,
    current_user=Depends(get_current_user)
):
    full_prompt=f"{SYSTEM_CONTENT}\n\nStudent_question:{request.question}"
    try:
        response=client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config=GENERATION_CONFIG,
        )
        return AskResponse(answer=response.text)
    except ValueError:
        raise HTTPException(status_code=400,detail="this question could not be answered,please change it")
    except Exception as e:
        print(f"Gemini error:{e}")
        raise HTTPException(status_code=503,detail="AI service is temporarily unavailable. Try again in a moment")
        