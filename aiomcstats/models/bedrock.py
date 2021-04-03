from typing import List
from pydantic import BaseModel

class Status(BaseModel):
    edition: str
    motd: List[str]
    protocol_version: int
    protocol_name: str
    player_count: int
    player_max: int
    server_id: int
    gamemode: str
    gamemode_int: int
    port_ipv4: int
    port_ipv6: int