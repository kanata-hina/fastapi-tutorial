from fastapi import FastAPI

api = FastAPI()


@api.get('/')
async def site_root():
    """root"""
    return {"message": "Hello, WORLD!"}

@api.get('/{id}')
async def id(id):
    return {"item_id": id}