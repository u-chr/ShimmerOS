import aiohttp
async def get_url(ide,ssl_ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://data.services.jetbrains.com/products/releases",ssl=ssl_ctx,params={
                                                                                                        'code': ide,
                                                                                                        'latest': 'true',
                                                                                                        'type': 'release'}) as resp:
            resp.raise_for_status()
            return (await resp.json())[ide][0]["downloads"]["windows"]["link"]