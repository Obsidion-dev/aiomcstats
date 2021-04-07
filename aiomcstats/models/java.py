from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID


class Debug(BaseModel):
    ping: bool
    query: bool
    srv: bool


class Info(BaseModel):
    raw: List[str]
    clean: List[str]
    html: List[str]


class Motd(BaseModel):
    raw: List[str]
    clean: List[str]
    html: List[str]


class Players(BaseModel):
    online: int
    max: int
    list: Optional[List[str]]
    uuid: Optional[Dict[str, UUID]]


class Mods(BaseModel):
    names: List[str]
    raw: Dict[str, str]


class Plugins(BaseModel):
    names: List[str]
    raw: Dict[str, str]


class Status(BaseModel):
    """Online status class."""

    online: bool
    ip: str
    port: int
    debug: Debug
    motd: Motd
    players: Players
    version: str
    map: str
    protocol: Optional[int]
    hostname: Optional[str]
    icon: Optional[str]
    software: Optional[str]
    plugins: Optional[Mods]
    mods: Optional[Plugins]
    info: Optional[Info]

class OfflineStatus(BaseModel):
    """Offline status class."""

    online: bool
    ip: str
    port: int
    debug: Debug
    hostname: Optional[str]
    error: str