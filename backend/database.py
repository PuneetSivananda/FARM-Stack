from model import Todo
import motor.motor_asyncio
import os
from dotenv import load_dotenv

""" Pymongo implementation
#Mongo driver
# from pymongo import MongoClient
# 
# "mongodb+srv://XXXX:XXXXXX@HOST/?retryWrites=true&w=majority" // Connection string latest
# "mongodb://XXXXXX:XXXXXX@HOSTNAME:27017,HOSTNAME:27017,HOSTNAME:27017/TodoList?ssl=true&replicaSet=atlas-c1pzxe-shard-0&authSource=admin&retryWrites=true&w=majority"
"""

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv('MONGO_URL')
)

database = client.TodoList
collection = database.todo


async def fetch_one_todo(title):
  document = collection.find_one({"title": title})
  return document


async def fetch_all_todos():
  todos = []
  cursor = collection.find({})
  limit = await collection.count_documents({})
  for document in await cursor.to_list(length=limit):
    todos.append(Todo(**document))
  return todos


async def create_todo(todo):
  document = todo
  result = await collection.insert_one(document)
  return result


async def update_todo(title, desc):
  await collection.update_one({"title": title}, {"$set": {
      "description": desc
  }})
  document = await collection.find_one({"title": title})
  return document


async def remove_todo(title):
  await collection.delete_one({"title": title})
  return True
