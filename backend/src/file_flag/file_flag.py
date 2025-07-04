# backend/src/file_flag/file_flag.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from datetime import datetime
import json

from task_queue.task_queue import task_queue, create_tasks

router = APIRouter()

class TaskCreate(BaseModel):
    type:    str = Field(..., example="MyType")
    content: str = Field(..., example="payload")
    name:    str = Field("None", example="TASK_NAME")

@router.post("/addTask", status_code=201)
async def __add_task(payload: TaskCreate):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_task = {
        "id": None,
        "status": "PENDING",
        "type": payload.type,
        "content": payload.content,
        "name": payload.name,
        "created_date": now
    }

    return await create_tasks(new_task)

@router.get("/getTask")
def __getTask():
    tasks = _load_tasks()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found.")
    return tasks[-1]
