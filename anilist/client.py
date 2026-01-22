import aiohttp
import json
class Client:
    URL = "https://graphql.anilist.co" 

    async def query(self, query: str, variables: dict = {}) -> dict:

        async with aiohttp.ClientSession() as session:
            async with session.post(self.URL, json={"query": query, "variables": variables}) as response:
                response.raise_for_status()
                return await response.json()
