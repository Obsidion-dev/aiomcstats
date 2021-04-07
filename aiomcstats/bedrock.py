from time import perf_counter
import asyncio_dgram
import struct
from .models.bedrock import BedrockStatus
import asyncio


request_status_data = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx"


def parse_response(data: bytes, latency: int) -> BedrockStatus:
    """Parse response

    Args:
        data (bytes): raw input
        latency (int): latency of request

    Returns:
        BedrockStatus: Status object
    """
    data = data[1:]
    name_length = struct.unpack(">H", data[32:34])[0]
    data = data[34 : 34 + name_length].decode().split(";")
    print(len(data))
    if len(data) == 7:
        return BedrockStatus(
            edition=data[0],
            motd=data[1],
            protocol_version=data[2],
            protocol_name=data[3],
            player_count=data[4],
            player_max=data[5],
            server_id=data[6],
            latency=latency,
        )
    return BedrockStatus(
        edition=data[0],
        motd=data[1],
        protocol_version=data[2],
        protocol_name=data[3],
        player_count=data[4],
        player_max=data[5],
        server_id=data[6],
        latency=latency,
        map=data[7],
        gamemode=data[8],
        gamemode_int=data[9],
        port_ipv4=data[10],
        port_ipv6=data[11],
    )


async def bedrock_status(host: str, port: int) -> BedrockStatus:
    """Get status of bedrock server

    Args:
        host (str): host
        port (int): port

    Returns:
        BedrockStatus: Status object
    """
    start = perf_counter()
    try:
        stream = await asyncio_dgram.connect((host, port))
        await stream.send(request_status_data)
        data, _ = await asyncio.wait_for(stream.recv(), 1)
    finally:
        try:
            stream.close()
        except BaseException:
            pass

    return parse_response(data, (perf_counter() - start))
