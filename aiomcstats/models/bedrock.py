from typing import List, Optional
from pydantic import BaseModel


class BedrockStatus(BaseModel):
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
    online: bool
    ip: str
    port: int
    hostname: str
    error: str
