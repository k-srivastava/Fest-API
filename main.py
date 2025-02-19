from fastapi import FastAPI

from router import event, pass_, team, user

app = FastAPI()
app.include_router(event.router)
app.include_router(pass_.router)
app.include_router(team.router)
app.include_router(user.router)


@app.get('/')
def root():
    return {'message': 'Hello Fest-API!'}
