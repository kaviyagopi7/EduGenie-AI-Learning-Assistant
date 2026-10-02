import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="EduGenie")

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


class Question(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
async def home():
    html_file = BASE_DIR / "templates" / "index.html"
    return html_file.read_text(encoding="utf-8")


@app.get("/health")
async def health():
    return {"status": "EduGenie is running!"}

@app.post("/quiz")
async def generate_quiz(data: Question):

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=f"""
Create a simple 5-question multiple-choice quiz about:
{data.question}

Give 4 options for each question and clearly mention the correct answer.
"""
        )

        return {
            "quiz": response.text
        }

    except Exception as e:

        return {
            "quiz": f"Error: {str(e)}"
        }
@app.post("/learning-path")
@app.post("/summarize")
async def summarize_text(data: Question):

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=f"""
Summarize the following educational text.

Make the summary:
- Short
- Simple
- Easy for students to understand
- Include the important points

Text:
{data.question}
"""
        )

        return {
            "summary": response.text
        }

    except Exception as e:

        return {
            "summary": f"Error: {str(e)}"
        }
async def learning_path(data: Question):

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=f"""
Create a simple personalized learning path for this topic:
{data.question}

Give the learning path in this order:
1. Beginner Basics
2. Core Concepts
3. Practice
4. Advanced Topics
5. Revision

Keep the explanation simple and student-friendly.
"""
        )

        return {
            "learning_path": response.text
        }

    except Exception as e:

        return {
            "learning_path": f"Error: {str(e)}"
        }
@app.post("/ask")
async def ask_question(data: Question):

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=data.question
        )

        return {
            "answer": response.text
        }

    except Exception as e:

        return {
            "answer": f"Error: {str(e)}"
        }