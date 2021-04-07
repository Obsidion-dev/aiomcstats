from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID


class Debug(BaseModel):
    """Info model

    Args:
        ping (bool): Wether ping succeeded
        query (bool): Wether query is enabled.
        srv (bool): Wether a srv record is used.
    """

    ping: bool
    query: bool
    srv: bool


class Info(BaseModel):
    """Info model

    Args:
        raw (List[str]): Raw info with minecraft formatting.
        clean (List[str]): Cleaned info without minecraft formatting.
        html (List[str]): Html info with html formatting.
    """

    raw: List[str]
    clean: List[str]
    html: List[str]


class Motd(BaseModel):
    """Info model

    Args:
        raw (List[str]): Raw motd with minecraft formatting.
        clean (List[str]): Cleaned motd without minecraft formatting.
        html (List[str]): Html motd with html formatting.
    """

    raw: List[str]
    clean: List[str]
    html: List[str]


class Players(BaseModel):
    """Info model

    Args:
        online (int): Current number of players online.
        max (int): Max number of players.
        list (Optional[List[str]]): Html info with html formatting.
        uuid (Optional[Dict[str, UUID]]): Html info with html formatting.
    """

    online: int
    max: int
    list: Optional[List[str]]
    uuid: Optional[Dict[str, UUID]]


class Mods(BaseModel):
    """Info model

    Args:
        names (List[str]): Names of current minecraft mods.
        raw (Dict[str, str]): Raw mod information.
    """

    names: List[str]
    raw: Dict[str, str]


class Plugins(BaseModel):
    """Info model

    Args:
        names (List[str]): Names of current minecraft plugins.
        raw (Dict[str, str]): Raw mod information.
    """

    names: List[str]
    raw: Dict[str, str]


class Status(BaseModel):
    """Info model

    Args:
        online (bool): Wether server online.
        ip (str): Ip address of server.
        port (int): Port of minecraft server.
        debug (Debug): Debug data.
        motd (Motd): Motd of server.
        players (Players): Players in the server.
        version (str): Version of protocol.
        map (str): Current map.
        protocol (Optional[int]): Protocol number.
        hostname (Optional[str]): Hostname of server.
        icon (Optional[str]): Favicon of server.
        software (Optional[str]): Software running server.
        plugins (Optional[Plugins]): Plugins installed.
        mods (Optional[Mods]): Mods installed.
        info (Optional[Info]): Info provided in players rather then players.
    """

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
    plugins: Optional[Plugins]
    mods: Optional[Mods]
    info: Optional[Info]


class OfflineStatus(BaseModel):
    """Info model

    Args:
        online: bool
        ip: str
        port: int
        debug: Debug
        hostname: Optional[str]
        error: str
    """

    online: bool
    ip: Optional[str]
    port: Optional[int]
    debug: Debug
    hostname: Optional[str]
    error: str
