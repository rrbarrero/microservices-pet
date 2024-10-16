from fastapi.responses import JSONResponse


class CommonStrategy:
    def __init__(self, http_client):
        self.client = http_client

    async def execute(self, method, url, headers, body, query_params):
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

            