from typing import List, Optional
from pydantic import BaseModel


class BedrockStatus(BaseModel):
    """Bedrock Status.

    Args:
        edition (str): Game edition.
        motd (str): Message of the day.
        protocol_version (int): Version of the game protocol.
        protocol_name (str): Protocol name.
        player_count (int): Current number of players on the server.
        player_max (int): Max number of servers on the server.
        server_id (int): Server id.
        latency (int): Latency from api.
        map (Optional[str]): Map. Defaults to None.
        gamemode (Optional[int]): Current gamemode. Defaults to None.
        gamemode_int (Optional[int]): Current gamemode id. Defaults to None.
        port_ipv4 (Optional[int]): Server port for ipv4. Defaults to None.
        port_ipv6 (Optional[int]): Server port for ipv6. Defaults to None.
    """

    edition: str
    motd: str
    protocol_version: int
    protocol_name: str
    player_count: int
    player_max: int
    server_id: int
    latency: int
    map: Optional[str] = None
    gamemode: Optional[int] = None
    gamemode_int: Optional[int] = None
    port_ipv4: Optional[int] = None
    port_ipv6: Optional[int] = None


class BedrockOffline(BaseModel):
    """Offline Bedrock Status.

    Args:
        online (boot): Wether server online.
        ip (boot): Ip of server.
        port (boot): Port of server.
        hostname (boot): Hostname of server.
        error (str): Error which the request failed on.
    """

    online: bool
    ip: str
    port: int
    hostname: str
    error: str
