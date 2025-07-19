from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

FILE_NAME = "students.json"

# Load existing students
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        students = json.load(f)
else:
    students = []

@app.get("/")
def home():
    return {"message": "Welcome"}

@app.post("/register")
def register(name: str = Form(...), roll: str = Form(...)):
    for student in students:
        if student["roll"] == roll:
            return {"error": f"Student with roll {roll} already exists."}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    student = {"name": name, "roll": roll, "timestamp": timestamp}
    students.append(student)

    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)

    return {"message": f"{name} registered successfully!", "total": len(students)}

@app.get("/students")
def get_students():
    return students

@app.delete("/delete/{roll}")
def delete_student(roll: str):
    global students
    students = [s for s in students if s["roll"] != roll]
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)
    return {"message": f"Student with roll {roll} deleted."}

@app.put("/update")
def update_student(
    old_roll: str = Form(...),
    new_name: str = Form(...),
    new_roll: str = Form(...)
):
    for student in students:
        if student["roll"] == old_roll:
            student["name"] = new_name
            student["roll"] = new_roll
            break
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)
    return {"message": f"Student with roll {old_roll} updated."}
