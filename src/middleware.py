from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import ipaddress


class BlackListMiddleware(BaseModel):
    blasklist: list[str]

async def blacklist_middleware(
    app: FastAPI,
    blacklist: BlackListMiddleware,
):
    async def middleware(request: Request, call_next):
        client_ip = request.client.host
        for network in blacklist.blacklist:
            if ipaddress.ip_address(client_ip) in ipaddress.ip_network(network):
                return JSONResponse(
                    status_code=403,
                    content={'message': 'Forbidden'}
                )
        response = await call_next(request)
        return response

    async def on_startup():
        app.middleware_stack.push(middleware)

    async def on_shutdown():
        app.middleware_stack.remove(middleware)

    return {
        "on_startup": on_startup,
        "on_shutdown": on_shutdown,
    }
