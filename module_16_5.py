from fastapi import FastAPI, Path, HTTPException, status, Body, Request, Form
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


users = []

app = FastAPI()

template = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return template.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return template.TemplateResponse("users.html", {"request": request, "user": users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.post("/user/{username}/{age}")
async def post_user(request: Request, user: User, username: Annotated[str
                   , Path(min_length=3, max_length=20
                    , description="Enter user name", examples="Andrey")]
                    , age: Annotated[int, Path(ge=18, le=100, discription="77")]) -> HTMLResponse:
    if users:

        user_id = max(users, key=lambda m: m.id).id + 1
    else:
        user_id = 0
    # user_username = username
    # user_age = age
    users.append(User(id=user_id, username=username, age=age))
    return template.TemplateResponse("users.html", {"request": request, "users": users})

@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: int, username: Annotated[str, Path(min_length=3, max_length=20
                    , description="Enter user name", examples="Andrey")]
                   , age: Annotated[int, Path(ge=1, le=10000)]) -> str:
    try:
        users[user_id].username = username
        users[user_id].age = age

        return f"User {users[user_id]} is updated"

    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id)

        return f"User ID={user_id} was deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

