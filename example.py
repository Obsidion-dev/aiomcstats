import asyncio
from aiomcstats import status, ping

print(asyncio.run(status("hypixel.net")))
