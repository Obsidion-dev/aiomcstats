"""Main Functions."""
from typing import Optional
from typing import Union

from aiomcstats.connection import TCPConnection
from aiomcstats.models.status import Debug
from aiomcstats.models.status import OfflineStatus
from aiomcstats.models.status import Status
from aiomcstats.server import Server
from aiomcstats.utils import create_status
from aiomcstats.utils import get_raw


async def ping(
    host: str, port: Optional[int] = None, tries: Optional[int] = 3
) -> Union[int, OfflineStatus]:
    """Ping minecraft server.

    Args:
        host (str): minecraft server address
        port (Optional[int], optional): port to query server otherwise
            it is found. Defaults to None.
        tries (Optional[int], optional): The amount of tries to get
            data from server. Defaults to 3.

    Returns:
        Union[int, OfflineStatus]: ping time or info.
    """
    hostname, port, ip, srv = await get_raw(host, port)
    connection = TCPConnection()
    await connection.connect(ip, port)
    exception = None
    for _attempt in range(tries):
        try:
            pinger = Server(connection, host=hostname, port=port)
            pinger.handshake()
            return await pinger.ping()
        except Exception as e:
            exception = str(e)
    else:
        debug = Debug(
            ping=True,
            query=False,
            srv=srv,
        )
        return OfflineStatus(
            online=False,
            ip=ip,
            port=port,
            debug=debug,
            hostname=hostname,
            error=exception,
        )


async def status(
    host: str, port: Optional[int] = None, tries: Optional[int] = 3
) -> Union[Status, OfflineStatus]:
    """Get status from Minecraft server.

    Args:
        host (str): minecraft server address
        port (Optional[int], optional): port to query server otherwise
            it is found. Defaults to None.
        tries (Optional[int], optional): The amount of tries to get
            data from server. Defaults to 3.

    Returns:
        Union[Status, OfflineStatus]: Online or Offline status object.
    """
    hostname, port, ip, srv = await get_raw(host, port)
    connection = TCPConnection()
    await connection.connect(ip, port)
    exception = None
    for _attempt in range(tries):
        try:
            pinger = Server(connection, host=hostname, port=port)
            pinger.handshake()
            result = await pinger.status()
            result["latency"] = await pinger.ping()
            data = create_status(result, ip, port, hostname, srv)
            return data
        except Exception as e:
            exception = str(e)
    else:
        debug = Debug(
            ping=True,
            query=False,
            srv=srv,
        )
        return OfflineStatus(
            online=False,
            ip=ip,
            port=port,
            debug=debug,
            hostname=hostname,
            error=exception,
        )
