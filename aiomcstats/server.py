"""Main packet logic."""

import datetime
import json
import random
from typing import Dict, Any
from aiomcstats.connection import Connection


class Server:
    """Server info class"""

    def __init__(
        self,
        connection: Connection,
        host: str = "127.0.0.1",
        port: int = 25565,
        version: int = 47,
        ping_token: int = None,
    ) -> None:
        """Minecraft server info.

        Args:
            connection (Connection): Connection to use
            host (str, optional): host address. Defaults to "".
            port (int, optional): minecraft server port. Defaults to 25565.
            version (int, optional): version. Defaults to 47.
            ping_token (int, optional): token to ping with. Defaults to None.
        """
        if ping_token is None:
            ping_token = random.randint(0, (1 << 63) - 1)
        self.version = version
        self.connection = connection
        self.host = host
        self.port = port
        self.ping_token = ping_token

    def handshake(self) -> None:
        """Handshake with server."""
        packet = Connection()
        packet.write_varint(0)
        packet.write_varint(self.version)
        packet.write_utf(self.host)
        packet.write_ushort(self.port)
        packet.write_varint(1)
        self.connection.write_buffer(packet)

    async def status(self) -> Dict[str, Any]:
        """Get status info of minecraft server.

        Raises:
            IOError: Received invalid status response packet.
            IOError: Received invalid JSON

        Returns:
            Dict[str, Any]: raw json response
        """
        request = Connection()
        request.write_varint(0)  # Request status
        self.connection.write_buffer(request)

        response = await self.connection.read_buffer()
        if response.read_varint() != 0:
            raise IOError("Received invalid status response packet.")
        try:
            raw = json.loads(response.read_utf())
        except ValueError:
            raise IOError("Received invalid JSON")
        return raw

    async def ping(self) -> int:
        """Ping minecraft server.

        Raises:
            IOError: Received invalid ping response packet.
            IOError: Received mangled ping response packet.

        Returns:
            int: ping of connection.
        """
        request = Connection()
        request.write_varint(1)  # Test ping
        request.write_long(self.ping_token)
        sent = datetime.datetime.now()
        self.connection.write_buffer(request)

        response = await self.connection.read_buffer()
        received = datetime.datetime.now()
        if response.read_varint() != 1:
            raise IOError("Received invalid ping response packet.")
        received_token = response.read_long()
        if received_token != self.ping_token:
            raise IOError(
                "Received mangled ping response packet (expected token %d, received %d)"
                % (self.ping_token, received_token)
            )

        delta = received - sent
        # We have no trivial way of getting a time delta :(
        return (
            delta.days * 24 * 60 * 60 + delta.seconds
        ) * 1000 + delta.microseconds / 1000.0
