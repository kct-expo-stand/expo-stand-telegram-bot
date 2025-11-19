import aiohttp
from config import SHEET_ENDPOINT

async def send_to_sheets(data):
    if not SHEET_ENDPOINT:
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SHEET_ENDPOINT, json=data, timeout=aiohttp.ClientTimeout(total=10)) as response:
                await response.text()
    except:
        pass
