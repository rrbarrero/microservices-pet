import random
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
from config import SERVICE_NAME, log
from etcd_client.client import EtcdClient
from health_check import health_check

app = FastAPI()

store_client = EtcdClient()
health_check.start(store_client)

def to_url(services: list[dict]):
    return [f"http://{x['address']}:{x['port']}" for x in services]


def get_random_replica_url() -> str:
    service_replicas = to_url(store_client.get_services(SERVICE_NAME))
    return random.choice(service_replicas)


@app.middleware("http")
async def authenticate_request(request: Request, call_next):

    # Simplified example (we omit authentication)
    response = await call_next(request)
    return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    
    replica_url = get_random_replica_url()
    log.debug(f"\n{replica_url=}\n")

    url = f"{replica_url}/{path}"

    method = request.method

    body = await request.body()

    headers = dict(request.headers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method,
                url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=5.0
            )

            return JSONResponse(
                status_code=response.status_code,
                content=response.json(),
                headers=response.headers
            )

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
