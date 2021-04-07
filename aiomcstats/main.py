from aiomcstats.models.bedrock import BedrockOffline, BedrockStatus

from aiomcstats.ping import Ping
from aiomcstats.utils import create_status, get_raw
from aiomcstats.models.java import Debug, OfflineStatus, Status
from typing import Optional, Union
from aiomcstats.bedrock import bedrock_status


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
    exception = ""
    try:
        hostname, port, ip, srv = await get_raw(host, port)
    except Exception as e:
        exception = str(e)
        debug = Debug(
        ping=False,
        query=False,
        srv=False,
        )
        return OfflineStatus(
            online=False,
            ip=host,
            port=port,
            debug=debug,
            hostname=host,
            error=exception,
        )
    for _ in range(tries):
        try:
            pinger = Ping(hostname, port)
            await pinger.connect()
            await pinger.handshake()
            result = await pinger.status()
            data = create_status(result, ip, port, hostname, srv)
            return data
        except Exception as e:
            exception = str(e)
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


async def bedrock(
    host: str, port: Optional[int] = 19132, tries: Optional[int] = 3
) -> Union[BedrockStatus, BedrockOffline]:
    """Get status from Minecraft Bedrock server.

    Args:
        host (str): minecraft server address
        port (Optional[int], optional): port to query server otherwise
            it is found. Defaults to None.
        tries (Optional[int], optional): The amount of tries to get
            data from server. Defaults to 3.

    Returns:
        Union[BedrockStatus, BedrockOffline]: Online or Offline status object.
    """

    exception = ""
    hostname, _, ip, _ = await get_raw(host, port)
    for _ in range(tries):
        try:
            return await bedrock_status(hostname, port)
        except Exception as e:
            exception = str(e)
    return BedrockOffline(
        online=False,
        ip=ip,
        port=port,
        hostname=hostname,
        error=exception,
    )
