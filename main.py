from fastapi import FastAPI

from router import pass_

app = FastAPI()
app.include_router(pass_.router)


@app.get("/")
async def root():
    return {'message': 'Hello World'}
