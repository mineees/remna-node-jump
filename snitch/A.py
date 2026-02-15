from collections import deque
from pathlib import Path


class A:
    filepath: Path = Path(__file__).resolve().parent / "volume" / "access.log"

    def detect(self, ip: str) -> str | None:
        if self.filepath.exists():
            with self.filepath.open() as file:
                for line in deque(file, maxlen=100):
                    if len(line.split(f"from {ip}:")) > 1:
                        email: str = line.split("email: ")[-1].split("\n")[0].strip()

                        return email if email != "" else None

        return None
