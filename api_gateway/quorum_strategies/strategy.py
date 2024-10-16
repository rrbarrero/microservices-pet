from typing import Protocol


class Strategy(Protocol):

    async def execute(self, method, url, headers, body, query_params):
        ...