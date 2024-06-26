from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

students = {

    1: {
        "name": 'Jhon',
        "age": 17,
        "year": "10"
    },
    2: {
        "name": "Doe",
        "age": 17,
        "class": "9"
    }

}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get('/')
def index():
    return {'name': "First Data"}


@app.get('/get-student/{student_id}')
def get_student(student_id: int = Path(..., description='Enter the id of student you want to view', gt=0, lt=6)):
    return students[student_id]


@app.get('/get-by-name')
def get_student(*, name: Optional[str] = None, test: int = None):
    for i in students:
        if students[i]['name'] == name:
            return students[i]
    return {"Data": "Not Found"}


@app.get('/get-by-path-query/{student_id}')
def get_student(*, student_id: int, name: Optional[str] = None, test: int = None):
    for i in students:
        if students[i]['name'] == name:
            return students[i]
    return {"Data": "Not Found"}


@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "students exist"}

    students[student_id] = student
    return students[student_id]


@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student doesnot exist"}

    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]


@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id in students:
        del students[student_id]
        return {'message':"Delete succesfully"}
    return {"Error": "Student doesnot exist"}
