"""Useful utils for different protocols."""
from aiomcstats.models.java import Debug, Info, Mods, Motd, Players, Status
from typing import Any, Dict, Optional
from typing import Tuple
import re

import dns.asyncresolver


async def get_raw(host: str, port: Optional[int] = None) -> Tuple[str, int, str, bool]:
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
        motd = Motd(
            raw=[raw["description"]["text"]],
            clean=[
                a.strip()
                for a in re.sub(r"(§.)", "", raw["description"]["text"]).split("\n")
            ],
            html=[ansi_to_html(raw["description"]["text"])],
        )
    elif "extra" in raw["description"]:
        motd = Motd(
            raw=[raw["description"]["extra"]],
            clean=["".join(element["extra"] for element in raw["description"])],
            html=[ansi_to_html(raw["description"]["extra"])],
        )
    elif type(raw["description"]) == str:
        motd = Motd(
            raw=[raw["description"]],
            clean=[
                a.strip() for a in re.sub(r"(§.)", "", raw["description"]).split("\n")
            ],
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
