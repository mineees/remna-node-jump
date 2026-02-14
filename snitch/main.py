from typing import Optional


def hex_to_ipv4(hex_str: str) -> str:
    """Little-endian hex → IPv4."""
    addr = int(hex_str, 16)
    return (
        f"{addr & 0xFF}."
        f"{(addr >> 8) & 0xFF}."
        f"{(addr >> 16) & 0xFF}."
        f"{(addr >> 24) & 0xFF}"
    )


def parse_ipv6_addr(hex_str: str) -> Optional[str]:
    """
    Парсит IPv6 адрес из /proc/net/tcp6.

    /proc/net/tcp6 хранит 32 hex символа = 16 байт.
    Но каждые 4 байта (32-bit слово) в little-endian!

    Пример из вашего сервера:
    Запись для [::ffff:178.205.75.101]:
      В /proc/net/tcp6: B2CD05650000000000000000FFFF0000
                        ^^^^^^^^ — первое слово, little-endian

    Нет, подождите. Формат такой:
    Каждое 32-bit слово в network byte order внутри,
    но порядок слов может варьироваться.

    Проще: берём 4 слова по 8 hex, каждое переворачиваем побайтово.
    """
    if len(hex_str) != 32:
        return None

    # Разбиваем на 4 слова по 8 hex (4 байта)
    words = [hex_str[i:i + 8] for i in range(0, 32, 8)]

    # Каждое слово переворачиваем (little-endian → big-endian)
    raw_bytes = []
    for w in words:
        b = bytes.fromhex(w)
        raw_bytes.extend(reversed(b))  # little-endian → big-endian

    # raw_bytes = 16 байт IPv6 адреса

    # Проверяем IPv4-mapped (::ffff:x.x.x.x)
    # Байты 0-9 = 0, байты 10-11 = 0xFF
    is_v4_mapped = (
        all(b == 0 for b in raw_bytes[:10]) and
        raw_bytes[10] == 0xFF and
        raw_bytes[11] == 0xFF
    )

    if is_v4_mapped:
        return f"{raw_bytes[12]}.{raw_bytes[13]}.{raw_bytes[14]}.{raw_bytes[15]}"

    # Полный IPv6
    groups = []
    for i in range(0, 16, 2):
        groups.append(f"{raw_bytes[i]:02x}{raw_bytes[i + 1]:02x}")
    return ":".join(groups)


def get_established_ips(port: int) -> set[str]:
    """
    Читает /proc/net/tcp И /proc/net/tcp6.
    Возвращает множество IP клиентов с ESTABLISHED-соединениями.
    """
    target_port_hex = f"{port:04X}"
    client_ips = set()

    # ── IPv4: /proc/net/tcp ──
    try:
        with open("/proc/net/tcp", "r") as f:
            next(f)
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue
                if parts[3] != "01":
                    continue

                local_port_hex = parts[1].split(":")[1]
                if local_port_hex.upper() != target_port_hex:
                    continue

                remote_ip_hex = parts[2].split(":")[0]
                ip = hex_to_ipv4(remote_ip_hex)
                client_ips.add(ip)
    except FileNotFoundError:
        pass

    # ── IPv6: /proc/net/tcp6 ──
    try:
        with open("/proc/net/tcp6", "r") as f:
            next(f)
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue
                if parts[3] != "01":
                    continue

                local_port_hex = parts[1].split(":")[1]
                if local_port_hex.upper() != target_port_hex:
                    continue

                remote_ip_hex = parts[2].split(":")[0]
                ip = parse_ipv6_addr(remote_ip_hex)
                if ip:
                    client_ips.add(ip)
    except FileNotFoundError:
        pass

    return client_ips


if __name__ == "__main__":
    port = int(input("Port: "))
    ips = get_established_ips(port)
    print(f"\nFound {len(ips)} unique clients:")
    for ip in sorted(ips):
        print(f"  {ip}")