```shell
chmod +x up.sh
```

```json
{
  "tag": "REMNAWAVE_API_INBOUND_PLAIN",
  "port": 61001,
  "listen": "127.0.0.1",
  "protocol": "dokodemo-door",
  "settings": {
    "address": "127.0.0.1"
  }
}
```

```json
{
  "inboundTag": [
    "REMNAWAVE_API_INBOUND_PLAIN"
  ],
  "outboundTag": "REMNAWAVE_API"
}
```

```yml
# docker-compose.yml:

ulimits:
  nofile:
    soft: 1048576 # ulimit -n
    hard: 1048576 # ulimit -Hn
```
