import aiohttp
from config import SHEET_ENDPOINT

async def send_to_sheets(data):
    if not SHEET_ENDPOINT:
        return
    async with aiohttp.ClientSession() as session:
        try:
            await session.post(SHEET_ENDPOINT, json=data)
        except:
            pass
