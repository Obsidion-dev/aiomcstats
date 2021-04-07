from aiomcstats import status
import asyncio

async def main():
    print(await status("hypixel.ne"))

asyncio.run(main())