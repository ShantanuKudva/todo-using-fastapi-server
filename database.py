from model import Todo

#mongodb driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.TodoList
collection = database.todo


async def fetch_one_todo(title):
    document = await collection.find_one({"title": title})
    return document

async def fetch_all_todo():
    res = []
    cursor = collection.find({})
    async for doc in cursor:
        res.append(Todo(**doc))
    return res

async def create_todo(todo):
    res = await collection.insert_one(todo)
    return res

async def update_todo(title,desc):
    await collection.update_one({"title": title}, {"$set":{
        "description": desc
    }})
    return await collection.find_one({"title": title})

async def remove_todo(title):
    response  = await collection.delete_one({"title": title})
    return response