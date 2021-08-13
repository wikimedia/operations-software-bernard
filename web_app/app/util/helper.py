import httpx
import json


async def make_api_call(endpoint):
    async with httpx.AsyncClient() as client:
        db_request = await client.get(endpoint)
        response = json.loads(db_request.text)
    return response
