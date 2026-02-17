### Быстрый старт

1. Клонировать репозиторий и перейти в папку проекта:

```shell
git clone git@github.com:timehollyname/Remnawave.git && cd ./Remnawave
```

2. Заполнить `.env` файл:

```shell
cp .env.example .env && nano .env
```

3. Разрешить запуск скрипта:

```shell
chmod +x up.sh
```

4. Запустить:

```
./up.sh
```

### Что делает `up.sh`

1. Проверяет, существует ли `.env` файл.
2. Проверяет, установлен ли `Docker` в системе.
    - Если `Docker` не установлен - устанавливает его.
3. Запускает стек через `docker-compose.yml`.

### Включение доступа к XRAY API (ВАЖНО)

#### Проблема

> Remnanode уже поднимает XRAY API на порту 61000, но к нему **нельзя получить доступ из‑за сертификатов (В новых версиях: remnawave/node)**.

#### Решение

> Создать новый `inbound` на другом порту (Например: `61001`) в панели `Remnawave` для нужного профиля.

##### Инструкция:

1. Добавить `inbound` в профиль:

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

2. Добавить `rule`:

```json
{
  "inboundTag": [
    "REMNAWAVE_API_INBOUND_PLAIN"
  ],
  "outboundTag": "REMNAWAVE_API"
}
```

3. Указать новые `HOST` и `PORT` в `.env`:

```
XRAY_API_HOST="127.0.0.1"
XRAY_API_PORT="61001"
```

### Настройка ulimits

В `docker-compose.yml` могут быть заданы лимиты открытых файловых дескрипторов:

```yml
ulimits:
  nofile:
    soft: 1048576
    hard: 1048576
```

Как проверить значения на хосте:

```shell
ulimit -n  # Текущее soft-значение
ulimit -Hn # Hard-лимит
```
