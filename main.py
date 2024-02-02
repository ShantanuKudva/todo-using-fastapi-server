from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo


app = FastAPI()

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


from database import (
fetch_one_todo,
fetch_all_todo,
create_todo,
update_todo,
remove_todo
)

@app.get("/")
def read_root():
    return {"Ping":"Pong"}

@app.get("/api/todo")
async def get_todos():
    response = await fetch_all_todo()
    return response

@app.get("/api/todo{title}", response_model = Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        print(response)
        return response
    else:
        raise HTTPException(404, f"There is no Todo Item with this title {title}")
    

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo):
    response = await create_todo(dict(todo))
    if response:
        print(response)
        return response
    else:
        raise HTTPException(400, f"Bad request")

@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title:str,desc:str):
    response  = await update_todo(title, desc)
    if response:
        print(response)
        return response
    else:
        raise HTTPException(404, f"There is no Todo Item with this title {title}")

@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response.deleted_count == 1:
        return {"message": "Todo item deleted successfully"}
    else:
        return {"error": f"Todo item with title {title} not found"}
