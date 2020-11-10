from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2

DATABASE_URL='postgresql://admin:admin@db:5432/db'

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
    #print(cursor)
    return {"message": "Hello, WORLD!"}

@api.get('/{id}/tasks')
async def getAllTasks(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM task where user_id = ' + str(id))
    rows = cur.fetchall()
    #print(rows)
    cur.close()
    conn.close()
    return {"item_id": id}

@api.post('/{id}/tasks')
async def createTask(id: int, task: Task):
    print(task)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO task(user_id, title, description) VALUES(" + str(id) + ", '" + task.title + "', '" + task.description + "')")
    conn.commit()
    cur.execute('SELECT * FROM task')
    rows = cur.fetchall()
    print(rows)
    cur.close()
    conn.close()
    return {"item_id": id}

@api.get('/{id}/tasks/{task_id}')
async def getAllTasks(id: int, task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM task where user_id = ' + str(id) + ' and id = ' + str(task_id))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise HTTPException(status_code=500, detail="task id not found")
    print(rows)
    cur.close()
    conn.close()
    return {"task_id": rows[0][0], "title": rows[0][2], "description": rows[0][3]}

@api.put('/{id}/tasks/{task_id}')
async def getAllTasks(id: int, task_id: int, task: Task):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE task SET title = '" + task.title + "', description = '" + task.description + "' where id = " + str(task_id) + " and user_id = " + str(id))
    conn.commit()
    cur.execute('SELECT * FROM task where user_id = ' + str(id) + ' and id = ' + str(task_id))
    rows = cur.fetchall()
    print(rows)
    cur.close()
    conn.close()
    return {"item_id": id}

@api.delete('/{id}/tasks')
async def getAllTasks(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE from task where user_id = " + str(id))
    conn.commit()
    cur.execute('SELECT * FROM task where user_id = ' + str(id))
    rows = cur.fetchall()
    print(rows)
    cur.close()
    conn.close()
    return {"item_id": id}