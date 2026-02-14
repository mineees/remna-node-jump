def hex_to_ipv4(hex: str) -> str:
    address = int(hex, 16)

    return (
        f"{(address) & 0xFF}."
        f"{(address >> 8) & 0xFF}."
        f"{(address >> 16) & 0xFF}."
        f"{(address >> 24) & 0xFF}"
    )

def get_established_ips(port: int) -> set[str]:
    """
    Читает /proc/net/tcp и возвращает IP клиентов
    с ESTABLISHED-соединениями к заданному порту.

    /proc/net/tcp формат:
      sl  local_address rem_address   st ...
      0: 00000000:01BB 0A0A0A01:C4E2 01 ...

    Адреса в hex little-endian, st=01 = ESTABLISHED
    01BB hex = 443 decimal
    """
    target_port_hex = f"{port:04X}"
    client_ips = set()

    # IPv4
    try:
        with open("/host/proc/net/tcp", "r") as f:
            next(f)  # заголовок
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue

                state = parts[3]
                if state != "01":  # не ESTABLISHED
                    continue

                local = parts[1]
                local_port_hex = local.split(":")[1]

                if local_port_hex.upper() != target_port_hex:
                    continue

                remote = parts[2]
                remote_ip_hex = remote.split(":")[0]
                ip = hex_to_ipv4(remote_ip_hex)
                client_ips.add(ip)
    except FileNotFoundError:
        pass

    return client_ips

if __name__ == '__main__':
    print(get_established_ips(443))
