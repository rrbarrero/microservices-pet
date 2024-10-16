import random
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
from quorum_strategies.common_strategy import CommonStrategy
from quorum_strategies.everyone_write_strategy import EveryoneWriteStrategy
from config import SERVICE_NAME, log
from etcd_client.client import EtcdClient
from health_check import health_check

app = FastAPI()

store_client = EtcdClient()
health_check.start(store_client)

def to_url(services: list[dict]):
    return [f"http://{x['address']}:{x['port']}" for x in services]


@app.middleware("http")
async def authenticate_request(request: Request, call_next):

    # Simplified example (we omit authentication)
    response = await call_next(request)
    return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    
    replicas = to_url(store_client.get_services(SERVICE_NAME))
    replica_url = random.choice(replicas)
    log.debug(f"\n{replica_url=}\n")

    url = f"{replica_url}/{path}"

    method = request.method

    body = await request.body()

    headers = dict(request.headers)

    async with httpx.AsyncClient() as client:
        try:
            match method:
                case "POST":
                    strategy = EveryoneWriteStrategy(client, replicas.copy(), path)
                case _:
                    strategy = CommonStrategy(client)
            return await strategy.execute(method, url, headers, body, request.query_params)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail="Error connecting to backend service")

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
