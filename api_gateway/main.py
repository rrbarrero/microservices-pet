from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

import itertools

app = FastAPI()

# Lista de réplicas de los microservicios
service_replicas = [
    "http://node_service:8000",  # Réplica 1 del servicio de tareas
]

# Iterador para balanceo de carga Round-Robin
replica_cycle = itertools.cycle(service_replicas)

# Middleware de autenticación (opcional)
@app.middleware("http")
async def authenticate_request(request: Request, call_next):
    # Aquí puedes implementar la lógica de autenticación
    # Por ejemplo, verificar un token JWT en las cabeceras
    # Si la autenticación falla, puedes lanzar un HTTPException

    # Ejemplo simplificado (omitimos autenticación)
    response = await call_next(request)
    return response

# Ruta genérica para redirigir solicitudes
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    # Obtener la URL de la réplica siguiente en el ciclo
    replica_url = next(replica_cycle)

    # Construir la URL completa
    url = f"{replica_url}/{path}"

    # Obtener el método HTTP de la solicitud
    method = request.method

    # Extraer el cuerpo de la solicitud
    body = await request.body()

    # Extraer las cabeceras
    headers = dict(request.headers)

    # Crear una nueva solicitud al servicio de destino
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

            # Construir la respuesta para el cliente
            return JSONResponse(
                status_code=response.status_code,
                content=response.json(),
                headers=response.headers
            )

        except httpx.RequestError as e:
            # Manejar errores de conexión
            raise HTTPException(status_code=502, detail="Error al conectar con el servicio de backend")

        except httpx.HTTPStatusError as e:
            # Manejar respuestas HTTP de error
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

# Manejo de excepciones generales
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )
