from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2

DATABASE_URL = 'postgresql://admin:admin@db:5432/db'


def get_connection():
    return psycopg2.connect(DATABASE_URL)


class Task(BaseModel):
    title: str
    description: str


api = FastAPI()


@api.get('/')
async def site_root():
    """root"""
    cursor = psycopg2.connect(DATABASE_URL)
    # print(cursor)
    return {"message": "Hello, WORLD!"}


@api.get('/{id}/tasks')
async def getAllTasks(id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM id where id = '" + id + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="user id not found")
    cur.execute("SELECT * FROM task where user_id = '" + id + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="task not found")
    tasks = [{"task_id": row[0], "title": row[2], "description": row[3]}
             for row in rows]
    cur.close()
    conn.close()
    return tasks


@api.post('/{id}/tasks')
async def createTask(id: str, task: Task):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM id where id = '" + id + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="user id not found")
    cur.execute("INSERT INTO task(user_id, title, description) VALUES('" + id + "', '" + task.title + "', '" + task.description + "') RETURNING id, title, description")
    conn.commit()
    task = cur.fetchone()
    if len(task) == 0:
        raise HTTPException(status_code=500, detail="task can not create")
    cur.close()
    conn.close()
    return {"task_id": task[0], "title": task[1], "description": task[2]}


@api.get('/{id}/tasks/{task_id}')
async def getAllTasks(id: str, task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM id where id = '" + id + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="user id not found")
    cur.execute("SELECT * FROM task where user_id = '" + id + "' and id = " + str(task_id))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="task id not found")
    cur.close()
    conn.close()
    return {"task_id": rows[0][0], "title": rows[0][2], "description": rows[0][3]}


@api.put('/{id}/tasks/{task_id}')
async def getAllTasks(id: str, task_id: int, task: Task):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM id where id = '" + id + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="user id not found")
    cur.execute("SELECT * FROM task where id = " + str(task_id))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="task id not found")
    cur.execute("UPDATE task SET title = '" + task.title + "', description = '" + task.description + "' where id = " + str(task_id) + " and user_id = '" + id + "' RETURNING title, description")
    conn.commit()
    task = cur.fetchone()
    if len(task) == 0:
        raise HTTPException(status_code=500, detail="task can not create")
    cur.close()
    conn.close()
    return {"title": task[0], "description": task[1]}


@api.delete('/{id}/tasks')
async def getAllTasks(id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM id where id = '" + id + "'")
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="user id not found")
    cur.execute("DELETE from task where user_id = '" + id + "'")
    conn.commit()
    cur.close()
    conn.close()
    return {}
