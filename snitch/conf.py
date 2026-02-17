from os import getenv
from pathlib import Path

__DIR__: Path = Path(__file__).resolve().parent

__OUTPUT_FILENAME__: str = "connections.log"
__OUTPUT_FILEPATH__: Path = __DIR__ / "volume" / __OUTPUT_FILENAME__

__XRAY_API_HOST__: str = str(getenv("XRAY_API_HOST", "127.0.0.1"))
__XRAY_API_PORT__: int = int(getenv("XRAY_API_PORT", "61000"))
__XRAY_API_ADDR__: str = f"{__XRAY_API_HOST__}:{__XRAY_API_PORT__}"

__XRAY_DOCKER_CONTAINER_NAME__: str = str(getenv("XRAY_DOCKER_CONTAINER_NAME", "remnanode"))

__POLLING_INTERVAL__: int = int(getenv("POLLING_INTERVAL", "1"))

__CONNECTION_DISCONNECT_TIMEOUT__: int = int(getenv("CONNECTION_DISCONNECT_TIMEOUT", "15"))
