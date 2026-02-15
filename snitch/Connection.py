class Connection:
    ip: str | None = None
    name: str | None = None
    connected_at: int | None = None
    disconnected_at: int | None = None
    duration: int | None = None

    def __init__(self, ip: str | None = None, name: str | None = None, connected_at: int | None = None, disconnected_at: int | None = None, duration: int | None = None):
        self.ip = ip
        self.name = name
        self.connected_at = connected_at
        self.disconnected_at = disconnected_at
        self.duration = duration

    def serialize(self) -> dict:
        return {
            'ip': self.ip,
            'name': self.name,
            'connected_at': self.connected_at,
            'disconnected_at': self.disconnected_at,
            'duration': self.duration,
        }
