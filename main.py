from fastapi import FastAPI

from router import pass_, team, user

app = FastAPI()
app.include_router(pass_.router)
app.include_router(team.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {'message': 'Hello World'}
