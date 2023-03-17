import json
import aiohttp
from pprint import pprint
from typing import Optional


class apitool:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def test_connection(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    print("Connection is working!")
                else:
                    print("Connection failed!")

    async def inspect_endpoint(self, endpoint: str, method: str = "GET", payload: Optional[dict] = None):
        url = self.base_url + endpoint
        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                request_coroutine = session.get(url, headers=headers)
            elif method.upper() == "POST":
                request_coroutine = session.post(url, headers=headers, json=payload)
            else:
                raise ValueError("Unsupported method")

            print(f"Request: {method.upper()} {url}")
            if payload:
                print("Payload:")
                pprint(payload)

            async with request_coroutine as response:
                print(f"Status: {response.status}")
                content = await response.json()
                print("Response:")
                pprint(content)

import asyncio

# Replace this URL with the base URL of your API
api_base_url = 'http://127.0.0.1:7860/'

# Create an instance of the apitool class
api_tool = apitool(api_base_url)
getend = 'controlnet/model_list'
postend = 'queue/satus'

# Run the async methods using asyncio
async def main():
    # Test connection
    await api_tool.test_connection()

    # Inspect a GET endpoint
    await api_tool.inspect_endpoint(getend)

    # Inspect a POST endpoint with an optional payload
    payload = {
        "key": "value"
        }
    #await api_tool.inspect_endpoint(postend, method="POST", payload=payload)

# Run the main function
#asyncio.run(main())