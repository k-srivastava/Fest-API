from fastapi import FastAPI, Depends

import security
from router import event, pass_, support_ticket, team, user

app = FastAPI()
app.include_router(event.router, dependencies=[Depends(security.verify_token)])
app.include_router(pass_.router, dependencies=[Depends(security.verify_token)])
app.include_router(support_ticket.router, dependencies=[Depends(security.verify_token)])
app.include_router(team.router, dependencies=[Depends(security.verify_token)])
app.include_router(user.router, dependencies=[Depends(security.verify_token)])


@app.get('/')
def root():
    return {'message': 'Hello Fest-API!'}
