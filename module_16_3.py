from fastapi import FastAPI, Path
from typing import Annotated

users = {'1': 'Имя: Duck-Nucken, возраст: 18'}

app = FastAPI()

@app.get("/users")
async def get_all_users() -> dict:
    return users

@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=2, max_length=20, description="Enter user name"
    , examples="Andrey")], age: Annotated[int, Path(ge=18, le=100, discription="77")]) -> str:
    current_id = str(int(max(users, key=str)) + 1)
    users[current_id] = f"Имя: {username}, возраст: {age}"
    return f"User {current_id} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: Annotated[int, Path(ge=1, le=10000)], username: Annotated[str
                   , Path(min_length=3, max_length=20, description="Enter user name", examples="Andrey")]
                   , age: Annotated[int, Path(ge=18, le=100, discription="77")]) -> str:
    user_id = str(user_id)
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is updated"

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=10000)]) -> str:
    user_id = str(user_id)
    users.pop(user_id)
    return f"User {user_id} has been deleted"

