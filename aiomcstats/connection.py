import struct
import asyncio
from typing import Any


class Connection:
    def __init__(self) -> None:
        self.sent = bytearray()
        self.received = bytearray()

    def read(self, length: int) -> bytearray:
        result = self.received[:length]
        self.received = self.received[length:]
        return result

    def write(self, data: bytearray) -> None:
        if isinstance(data, Connection):
            data = bytearray(data.flush())
        if isinstance(data, str):
            data = bytearray(data)
        self.sent.extend(data)

    def receive(self, data: bytearray) -> None:
        if not isinstance(data, bytearray):
            data = bytearray(data)
        self.received.extend(data)

    def remaining(self) -> int:
        return len(self.received)

    def flush(self) -> bytearray:
        result = self.sent
        self.sent = ""
        return result

    def _unpack(self, format, data) -> Any:
        return struct.unpack(">" + format, bytes(data))[0]

    def _pack(self, format, data) -> bytes:
        return struct.pack(">" + format, data)

    def read_varint(self) -> int:
        result = 0
        for i in range(5):
            part = ord(self.read(1))
            result |= (part & 0x7F) << 7 * i
            if not part & 0x80:
                return result
        raise IOError("Server sent a varint that was too big!")

    def write_varint(self, value) -> None:
        remaining = value
        for i in range(5):
            if remaining & ~0x7F == 0:
                self.write(struct.pack("!B", remaining))
                return
            self.write(struct.pack("!B", remaining & 0x7F | 0x80))
            remaining >>= 7
        raise ValueError("The value %d is too big to send in a varint" % value)

    def read_utf(self) -> bytearray:
        length = self.read_varint()
        return self.read(length).decode("utf8")

    def write_utf(self, value) -> None:
        self.write_varint(len(value))
        self.write(bytearray(value, "utf8"))

    def read_ascii(self):
        result = bytearray()
        while len(result) == 0 or result[-1] != 0:
            result.extend(self.read(1))
        return result[:-1].decode("ISO-8859-1")

    def write_ascii(self, value) -> None:
        self.write(bytearray(value, "ISO-8859-1"))
        self.write(bytearray.fromhex("00"))

    def read_short(self) -> Any:
        return self._unpack("h", self.read(2))

    def write_short(self, value) -> None:
        self.write(self._pack("h", value))

    def read_ushort(self) -> Any:
        return self._unpack("H", self.read(2))

    def write_ushort(self, value) -> None:
        self.write(self._pack("H", value))

    def read_int(self) -> Any:
        return self._unpack("i", self.read(4))

    def write_int(self, value) -> None:
        self.write(self._pack("i", value))

    def read_uint(self) -> Any:
        return self._unpack("I", self.read(4))

    def write_uint(self, value) -> None:
        self.write(self._pack("I", value))

    def read_long(self) -> Any:
        return self._unpack("q", self.read(8))

    def write_long(self, value) -> None:
        self.write(self._pack("q", value))

    def read_ulong(self) -> Any:
        return self._unpack("Q", self.read(8))

    def write_ulong(self, value) -> None:
        self.write(self._pack("Q", value))

    def read_buffer(self):
        length = self.read_varint()
        result = Connection()
        result.receive(self.read(length))
        return result

    def write_buffer(self, buffer) -> None:
        data = buffer.flush()
        self.write_varint(len(data))
        self.write(data)


class TCPConnection(Connection):
    def __init__(self) -> None:
        Connection.__init__(self)

    async def connect(self, host: str, port: int, timeout: int = 3) -> None:
        conn = asyncio.open_connection(host, port)
        self.reader, self.writer = await asyncio.wait_for(conn, timeout=timeout)

    async def read(self, length) -> bytearray:
        result = bytearray()
        while len(result) < length:
            new = await self.reader.read(length - len(result))
            if len(new) == 0:
                raise IOError("Server did not respond with any information!")
            result.extend(new)
        return result

    def write(self, data) -> None:
        self.writer.write(data)

    async def read_varint(self) -> int:
        result = 0
        for i in range(5):
            part = ord(await self.read(1))
            result |= (part & 0x7F) << 7 * i
            if not part & 0x80:
                return result
        raise IOError("Server sent a varint that was too big!")

    async def read_utf(self):
        length = await self.read_varint()
        return self.read(length).decode("utf8")

    async def read_ascii(self):
        result = bytearray()
        while len(result) == 0 or result[-1] != 0:
            result.extend(await self.read(1))
        return result[:-1].decode("ISO-8859-1")

    async def read_short(self) -> Any:
        return self._unpack("h", await self.read(2))

    async def read_ushort(self) -> Any:
        return self._unpack("H", await self.read(2))

    async def read_int(self) -> Any:
        return self._unpack("i", await self.read(4))

    async def read_uint(self) -> Any:
        return self._unpack("I", await self.read(4))

    async def read_long(self) -> Any:
        return self._unpack("q", await self.read(8))

    async def read_ulong(self) -> Any:
        return self._unpack("Q", await self.read(8))

    async def read_buffer(self) -> Connection:
        length = await self.read_varint()
        result = Connection()
        result.receive(await self.read(length))
        return result
