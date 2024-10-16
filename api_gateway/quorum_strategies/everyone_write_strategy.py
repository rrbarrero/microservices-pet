from fastapi.responses import JSONResponse


class EveryoneWriteStrategy:
    def __init__(self, http_client, replicas, path):
        self.client = http_client
        self.replicas = replicas
        self.path = path

    async def execute(self, method, _, headers, body, query_params):
        for replica_url in self.replicas:
            url = f"{replica_url}/{self.path}"
            response = await self.client.request(
                method,
                url,
                headers=headers,
                content=body,
                params=query_params,
                timeout=5.0
            )

        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
            headers=response.headers
        )