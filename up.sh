#!/usr/bin/env bash

set -euo pipefail

info() {
    echo "\033[0;34m[INFO]\033[0m $(date '+%H:%M:%S') $*";
}

success() {
    echo "\033[0;32m[SUCCESS]\033[0m $(date '+%H:%M:%S') $*";
}

warning() {
    echo "\033[0;33m[WARNING]\033[0m $(date '+%H:%M:%S') $*";
}

fail() {
    echo "\033[0;31m[FAIL]\033[0m $(date '+%H:%M:%S') $*" >&2; exit 1;
}

run() {
    env
    setupDockerCompose
    upDockerCompose
}

env() {
    info "Проверка существование [.env] файла..."

    if [[ -f ".env" ]]; then
        success "Файл [.env] найден."
    else
        fail "Файл [.env] не найден."
    fi
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
