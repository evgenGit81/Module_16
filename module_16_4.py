from fastapi import FastAPI, Path, HTTPException, status, Body
from pydantic import BaseModel
from typing import Annotated, List


users = []

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/users")
async def get_all_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
async def post_user(user: User, username: Annotated[str
                   , Path(min_length=3, max_length=20
                    , description="Enter user name", examples="Andrey")]
                    , age: Annotated[int, Path(ge=18, le=100, discription="77")]) -> str:
    user.id = len(users) + 1
    user.username = username
    user.age = age
    users.append(user)
    return f"User {user} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: int, username: Annotated[str, Path(min_length=3, max_length=20
                    , description="Enter user name", examples="Andrey")]
                   , age: Annotated[int, Path(ge=1, le=10000)]) -> str:
    try:
        users[user_id - 1].username = username
        users[user_id - 1].age = age

        return f"User {users[user_id]} is updated"

    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id - 1)

        return f"User ID={user_id} was deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

