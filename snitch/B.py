class B:
    def hex_to_ipv4(self, hex: str) -> str:
        addr: int = int(hex, 16)

        return (
            f"{(addr) & 0xFF}."
            f"{(addr >> 8) & 0xFF}."
            f"{(addr >> 16) & 0xFF}."
            f"{(addr >> 24) & 0xFF}"
        )

    def hex_to_ipv6(self, hex: str) -> str | None:
        if len(hex) != 32:
            return None

        words: list = [hex[i:i + 8] for i in range(0, 32, 8)]

        raw_bytes: list = []
        for w in words:
            b: bytes = bytes.fromhex(w)
            raw_bytes.extend(reversed(b))

        is_v4_mapped: bool = (
            all(b == 0 for b in raw_bytes[:10]) and
            raw_bytes[10] == 0xFF and
            raw_bytes[11] == 0xFF
        )

        if is_v4_mapped:
            return f"{raw_bytes[12]}.{raw_bytes[13]}.{raw_bytes[14]}.{raw_bytes[15]}"

        groups: list = []
        for i in range(0, 16, 2):
            groups.append(f"{raw_bytes[i]:02x}{raw_bytes[i + 1]:02x}")

        return ":".join(groups)

    def get(self, ports: list) -> set:
        ports: list = [f"{port:04X}" for port in ports]
        collection: set = set()

        try:
            with open("/proc/net/tcp", "r") as f:
                next(f)

                for line in f:
                    parts: list = line.strip().split()

                    if len(parts) < 4 or parts[3] != "01":
                        continue

                    local_port_hex: str = parts[1].split(":")[1]

                    if local_port_hex.upper() not in ports:
                        continue

                    remote_ip_hex: str = parts[2].split(":")[0]
                    collection.add(self.hex_to_ipv4(remote_ip_hex))

        except FileNotFoundError:
            pass

        try:
            with open("/proc/net/tcp6", "r") as f:
                next(f)

                for line in f:
                    parts: list = line.strip().split()

                    if len(parts) < 4 or parts[3] != "01":
                        continue

                    local_port_hex: str = parts[1].split(":")[1]

                    if local_port_hex.upper() not in ports:
                        continue

                    remote_ip_hex: str = parts[2].split(":")[0]
                    ip: str | None = self.hex_to_ipv6(remote_ip_hex)

                    if ip:
                        collection.add(ip)

        except FileNotFoundError:
            pass

        return collection
