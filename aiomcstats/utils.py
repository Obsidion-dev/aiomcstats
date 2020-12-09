"""Useful utils for different protocols."""
import re
from ipaddress import ip_address
from typing import Any
from typing import Dict
from typing import Tuple
from urllib.parse import urlparse

import dns.asyncresolver
from aiomcstats.models.status import Debug
from aiomcstats.models.status import Info
from aiomcstats.models.status import Mods
from aiomcstats.models.status import Players
from aiomcstats.models.status import Status


async def get_raw(host: str, port: int = None) -> Tuple[str, int, str, bool]:
    """Get raw info on port

    Args:
        host (str): hostname
        port (int, optional): port to use. Defaults to None.

    Raises:
        ValueError: Error if invalid address

    Returns:
        Tuple[str, int, str, bool]: hostname, port, ip, wether srv used
    """
    srv = False
    if ":" in host:
        parts = host.split(":")
        if len(parts) > 2:
            raise ValueError("Invalid address '%s'" % host)
        host = parts[0]
        port = int(parts[1])
    if port is None:
        port = 25565
        try:
            answers = await dns.asyncresolver.resolve(
                "_minecraft._tcp." + host, "SRV", search=True
            )
            if len(answers):
                answer = answers[0]
                host = str(answer.target).rstrip(".")
                port = int(answer.port)
                srv = True
        except Exception:
            pass

    ip = (await dns.asyncresolver.resolve(host, "A", search=True))[0].address

    return (host, port, ip, srv)


def ip_type(address: str) -> int:
    """Determine wether ipv4 or ipv6

    Args:
        address (str): ip address

    Returns:
        Union[int]: type of ip
    """
    try:
        return ip_address(address).version
    except ValueError:
        return None


def parse_address(address: str) -> Tuple[str, int]:
    """Parse string url to get host and port.

    Args:
        address (str): web address

    Raises:
        ValueError: If invalid address

    Returns:
        Tuple[str, int]: hostname and port
    """
    tmp = urlparse("//" + address)
    if not tmp.hostname:
        raise ValueError("Invalid address '%s'" % address)
    return (tmp.hostname, tmp.port)


COLOR_DICT = {
    "31": [(255, 0, 0), (128, 0, 0)],
    "32": [(0, 255, 0), (0, 128, 0)],
    "33": [(255, 255, 0), (128, 128, 0)],
    "34": [(0, 0, 255), (0, 0, 128)],
    "35": [(255, 0, 255), (128, 0, 128)],
    "36": [(0, 255, 255), (0, 128, 128)],
}

COLOR_REGEX = re.compile(r"\[(?P<arg_1>\d+)(;(?P<arg_2>\d+)(;(?P<arg_3>\d+))?)?m")

BOLD_TEMPLATE = '<span style="color: rgb{}; font-weight: bolder">'
LIGHT_TEMPLATE = '<span style="color: rgb{}">'


def ansi_to_html(text: str) -> str:
    """Convert minecraft formatting to html.

    Args:
        text (str): Raw minecraft text

    Returns:
        str: html formatted text
    """
    text = text.replace("[m", "</span>")

    def single_sub(match):
        argsdict = match.groupdict()
        if argsdict["arg_3"] is None:
            if argsdict["arg_2"] is None:
                color, bold = argsdict["arg_1"], 0
            else:
                color, bold = argsdict["arg_1"], int(argsdict["arg_2"])
        else:
            color, bold = argsdict["arg_2"], int(argsdict["arg_3"])

        if bold:
            return BOLD_TEMPLATE.format(COLOR_DICT[color][1])
        return LIGHT_TEMPLATE.format(COLOR_DICT[color][0])

    return COLOR_REGEX.sub(single_sub, text)


def create_status(
    raw: Dict[str, Any], ip: str, port: int, hostname: str, srv: bool
) -> Status:
    """Create status object from json.

    Args:
        raw (Dict[str, Any]): raw json
        ip (str): ip of server
        port (int): port of server
        hostname (str): hostname of server
        srv (bool): wether srv used

    Returns:
        Status: Status object
    """
    icon = raw["favicon"] if "favicon" in raw else None
    software = raw["software"] if "software" in raw else None
    protocol = raw["version"]["protocol"]
    version = raw["version"]["name"]
    map = raw["map"] if "map" in raw else "world"
    debug = Debug(
        ping=True,
        query=False,
        srv=srv,
    )
    if "text" in raw["description"]:
        motd = Info(
            raw=[raw["description"]["text"]],
            clean=[re.sub(r"(§.)", "", raw["description"]["text"])],
            html=[ansi_to_html(raw["description"]["text"])],
        )
    elif "extra" in raw["description"]:
        motd = Info(
            raw=[raw["description"]["text"]],
            clean=["".join(element["text"] for element in raw["description"])],
            html=[ansi_to_html(raw["description"]["text"])],
        )
    elif type(raw["description"]) == str:
        motd = Info(
            raw=[raw["description"]],
            clean=[re.sub(r"(§.)", "", raw["description"])],
            html=[ansi_to_html(raw["description"])],
        )

    info = None
    if "sample" not in raw["players"]:
        players = Players(online=raw["players"]["online"], max=raw["players"]["max"])
    elif len(raw["players"]["sample"]) == 0:
        players = Players(online=raw["players"]["online"], max=raw["players"]["max"])
    elif "00000000-0000-0000-0000-000000000000" in raw["players"]["sample"]:
        info = Info()
        players = Players(online=raw["players"]["online"], max=raw["players"]["max"])
    else:
        players = Players(
            online=raw["players"]["online"],
            max=raw["players"]["max"],
            list=[i["name"] for i in raw["players"]["sample"]],
            uuid={name["name"]: name["id"] for name in raw["players"]["sample"]},
        )
    plugins = Mods() if "plugins" in raw else None
    mods = None
    if "modinfo" in raw:
        mods = Mods(
            names=[i["modid"] for i in raw["modinfo"]["modList"]],
            raw={name["modid"]: name["version"] for name in raw["modinfo"]["modList"]},
        )

    data = Status(
        online=True,
        ip=ip,
        port=port,
        debug=debug,
        motd=motd,
        players=players,
        version=version,
        map=map,
        protocol=protocol,
        hostname=hostname,
        icon=icon,
        software=software,
        plugins=plugins,
        mods=mods,
        info=info,
    )
    return data
