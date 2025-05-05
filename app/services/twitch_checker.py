import aiohttp
from services.env_loader import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

TWITCH_USER_LOGIN = "furiatv"
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_STREAM_URL = "https://api.twitch.tv/helix/streams"

access_token = None

async def get_access_token():
    global access_token
    if access_token:
        return access_token
    async with aiohttp.ClientSession() as session:
        async with session.post(TWITCH_TOKEN_URL, params={
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }) as resp:
            data = await resp.json()
            access_token = data.get("access_token")
            return access_token

async def is_furia_live():
    global access_token
    token = await get_access_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(TWITCH_STREAM_URL, headers=headers, params={"user_login": TWITCH_USER_LOGIN}) as resp:
            if resp.status == 401:
                access_token = None  # Token expirado, forçar refresh
                return await is_furia_live()
            data = await resp.json()
            return bool(data.get("data"))
