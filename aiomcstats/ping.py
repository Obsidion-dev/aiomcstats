import random
import time
import json
from typing import Any, Dict

from aiomcstats.connection import TCPConnection
from aiomcstats.connection import Connection


class Ping:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def connect(self) -> None:
        self.connection = TCPConnection()
        await self.connection.connect(self.host, self.port)

    async def handshake(self) -> None:
        packet = Connection()
        packet.write_varint(0)
        packet.write_varint(47)
        packet.write_utf(self.host)
        packet.write_ushort(self.port)
        packet.write_varint(1)
        self.connection.write_buffer(packet)

    async def status(self) -> Dict[str, Any]:
        request = Connection()
        request.write_varint(0)  # Request status

        sent = time.time()
        self.connection.write_buffer(request)

        response = await self.connection.read_buffer()
        received = time.time()
        if response.read_varint() != 0:
            raise IOError("Received invalid status response packet.")
        try:
            raw: Dict[str, Any] = json.loads(response.read_utf())
        except ValueError:
            raise IOError("Received invalid JSON")
        raw["latency"] = received - sent
        return raw
