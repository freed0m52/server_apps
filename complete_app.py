from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
import re

app = FastAPI()

# ========== ЗАДАНИЕ 1.1 ==========
@app.get("/")
async def root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}

# ========== ЗАДАНИЕ 1.2 ==========
@app.get("/html")
async def get_html():
    return FileResponse("index.html")

# ========== ЗАДАНИЕ 1.3 ==========
class Numbers(BaseModel):
    num1: float
    num2: float

@app.post("/calculate")
async def calculate(numbers: Numbers):
    result = numbers.num1 + numbers.num2
    return {"result": result}

# ========== ЗАДАНИЕ 1.4 ==========
class User(BaseModel):
    name: str
    id: int

default_user = User(name="Иван Петров", id=1)

@app.get("/users")
async def get_users():
    return default_user

# ========== ЗАДАНИЕ 1.5 ==========
class UserAge(BaseModel):
    name: str
    age: int

@app.post("/user")
async def check_user(user: UserAge):
    is_adult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }

# ========== ЗАДАНИЕ 2.1 ==========
class Feedback(BaseModel):
    name: str
    message: str

feedbacks = []

@app.post("/feedback")
async def create_feedback(feedback: Feedback):
    feedbacks.append(feedback)
    return {"message": f"Feedback received. Thank you, {feedback.name}."}

@app.get("/feedbacks")
async def get_feedbacks():
    return {"feedbacks": feedbacks}

# ========== ЗАДАНИЕ 2.2 ==========
class ValidatedFeedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)
    
    @field_validator('message')
    @classmethod
    def check_forbidden_words(cls, v: str) -> str:
        forbidden_words = ["крингк", "рофл", "вайб"]
        message_lower = v.lower()
        for word in forbidden_words:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, message_lower):
                raise ValueError(f"Использование недопустимых слов. Слово '{word}' запрещено")
        return v

validated_feedbacks = []

@app.post("/feedback-validated")
async def create_validated_feedback(feedback: ValidatedFeedback):
    validated_feedbacks.append(feedback)
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}

@app.get("/feedbacks-validated")
async def get_validated_feedbacks():
    return {"feedbacks": validated_feedbacks}