#!/usr/bin/env bash

set -euo pipefail

info() {
    echo "[INFO] $(date '+%H:%M:%S') $*";
}

success() {
    echo "[SUCCESS] $(date '+%H:%M:%S') $*";
}

warning() {
    echo "[WARNING] $(date '+%H:%M:%S') $*";
}

fail() {
    echo "[FAIL] $(date '+%H:%M:%S') $*" >&2; exit 1;
}

run() {
    env
    setupDockerCompose
    upDockerCompose
}

env() {
    info "Проверка существование [.env] файлов..."

    for dir in remnanode snitch; do
        if [[ -f "$dir/.env" ]]; then
            success "Файл [$dir/.env] найден."
        else
            fail "Файл [$dir/.env] не найден."
        fi
    done
}

upDockerCompose() {
    info "Сборка и запуск [docker-compose.yml]..."

    if docker compose up -d --build; then
        success "[docker-compose.yml] успешно запущен."
    else
        fail "Произошла ошибка при запуске [docker-compose.yml]."
    fi
}

setupDockerCompose() {
    info "Проверка Docker Compose..."

    if docker compose version &>/dev/null; then
        success "Docker Compose [$(docker compose version --short)] установлен."
    else
        warning "Docker Compose не найден, начинаю установку..."

        info "Скачивание установочного скрипта в [/tmp/get-docker.sh]..."

        if output=$(curl -fsSL https://get.docker.com -o /tmp/get-docker.sh 2>&1); then
            success "Установочный скрипт доступен по пути: /tmp/get-docker.sh"
        else
            fail "Произошла ошибка при скачивании установочного скрипта:\n$output"
        fi

        info "Запуск установочного скрипта [/tmp/get-docker.sh]..."

        if output=$(sh /tmp/get-docker.sh 2>&1); then
            success "Установочный скрипт выполнен."
        else
            fail "Произошла ошибка при установке Docker:\n$output"
        fi

        info "Удаление установочного скрипта [/tmp/get-docker.sh]..."

        if output=$(rm -f /tmp/get-docker.sh 2>&1); then
            success "Установочный скрипт удалён."
        else
            fail "Произошла ошибка при удалении установочного скрипта:\n$output"
        fi

        if docker compose version &>/dev/null; then
            success "Docker Compose [$(docker compose version --short)] успешно установлен."
        else
            fail "Произошла ошибка, Docker Compose недоступен."
        fi
    fi
}

run
