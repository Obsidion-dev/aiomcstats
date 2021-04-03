
from time import perf_counter
import asyncio_dgram
import socket
import struct
from .models.bedrock import Status

class BedrockServerStatus:
    request_status_data = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x124Vx'

    def __init__(self, host, port=19132, timeout=3):
        self.host = host
        self.port = port
        self.timeout = timeout

    @staticmethod
    def parse_response(data: bytes, latency: int):
        data = data[1:]
        name_length = struct.unpack('>H', data[32:34])[0]
        data = data[34:34+name_length].decode().split(';')
        edition: str
        return Status(
            edition=data[0],motd=[data[1], data[7]], protocol_version=data[2], 
            protocol_name=data[3], player_count=data[4],player_max=data[5],server_id=data[6],
            gamemode=data[8],gamemode_int=data[9],port_ipv4=data[10], port_ipv6=data[11])

    async def read_status_async(self):
        start = perf_counter()

        try:
            stream = await asyncio_dgram.connect((self.host, self.port))
            await stream.send(self.request_status_data)
            data, _ = await stream.recv()
        finally:
            try:
                stream.close()
            except BaseException:
                pass

        return self.parse_response(data, (perf_counter() - start))