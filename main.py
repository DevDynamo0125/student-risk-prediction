from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime

import joblib




# Load trained model
model = joblib.load("model.pkl")

app = FastAPI(title="Student Risk Prediction API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = MongoClient("mongodb://localhost:27017")
db = client["student-ai"]
collection = db["prediction"]



# Input schema (what frontend sends)
class StudentData(BaseModel):
    attendance: int
    study_hours: int
    previous_marks: int
    assignment_completion: int

@app.get("/")
def home():
    return {"message": "Student Risk Prediction API is running"}

@app.post("/predict")
def predict_risk(student: StudentData):
    features = [[
        student.attendance,
        student.study_hours,
        student.previous_marks,
        student.assignment_completion
    ]]

    result = model.predict(features)[0]
    risk_value = "YES" if result == 1 else "NO"

    # ✅ SAVE TO MONGODB
    collection.insert_one({
        "attendance": student.attendance,
        "study_hours": student.study_hours,
        "previous_marks": student.previous_marks,
        "assignment_completion": student.assignment_completion,
        "risk": risk_value,
        "created_at": datetime.utcnow()
    })

    return {
        "risk": risk_value
    }
