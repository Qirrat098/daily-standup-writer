from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Home route
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

# Generate standup
@app.post("/generate")
async def generate(
    request: Request,
    yesterday: str = Form(...),
    today: str = Form(...),
    blockers: str = Form(...),
    tone: str = Form(...)
):
    prompt = f"""
    Act as a software engineer writing a daily standup.

    Make it:
    - Clear
    - Concise
    - Professional
    - Bullet-point formatted

    Tone: {tone}

    Yesterday:
    {yesterday}

    Today:
    {today}

    Blockers:
    {blockers}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ updated model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        output = response.choices[0].message.content

    except Exception as e:
        output = f"Error: {str(e)}"

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "result": output
        }
    )