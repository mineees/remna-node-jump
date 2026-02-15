from pathlib import Path
from time import sleep, time

from A import A
from B import B
from Connection import Connection
from ConnectionMap import ConnectionMap

c: ConnectionMap = ConnectionMap()
d: ConnectionMap = ConnectionMap()

if __name__ == "__main__":
    a: A = A()
    b: B = B()

    dir: Path = Path(__file__).resolve().parent
    volume: Path = dir / "volume"

    while True:
        sleep(1)

        connections: set = b.get([443, 2053])

        for ip in connections:
            if not c.exists(ip):
                c.add(Connection(ip=ip, connected_at=int(time())))

        for connection in c.to_list():
            connection.duration = int(time()) - connection.connected_at

            if connection.name is None:
                name: str | None = a.detect(ip)

                if name is not None:
                    connection.name = name

            if connection.ip not in connections:
                connection.disconnected_at = int(time())
                connection.duration = connection.disconnected_at - connection.connected_at

                d.add(connection)
                c.delete(connection.ip)

        with (volume / "c.json").open("w") as file:
            file.write(c.to_str())

        with (volume / "d.json").open("w") as file:
            file.write(d.to_str())
