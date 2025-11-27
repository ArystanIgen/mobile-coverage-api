#!/bin/bash

wait_for () {
    echo "waiting for $1:$2"
    for _ in `seq 0 100`; do
        (echo > /dev/tcp/$1/$2) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$1:$2 accepts connections"
            break
        fi
        sleep 1
    done
}

alembic_migration() {
  alembic -x data=true upgrade head
}

wait_for_db() {
  wait_for "${DB_HOST}" "${DB_PORT}"
}


case "$ENV" in
"LINT")
    echo '===RUN MYPY===' && mypy .
    echo '===RUN RUFF===' && ruff check --no-cache .
    echo '===RUN BANDIT===' && bandit .
    echo '===RUN SAFETY CHECK===' && safety check --full-report --ignore 42194
    ;;
"TEST")
    wait_for_db
    pytest .
    ;;
"DEV")
    wait_for_db
    alembic_migration
    uvicorn app.main:main_app \
        --reload \
        --host "${UVICORN_HOST:-0.0.0.0}" \
        --port "${UVICORN_PORT:-8000}" \
        --no-access-log
    ;;

"PRODUCTION")
    wait_for_db
    alembic_migration
    uvicorn app.main:main_app \
        --host "${UVICORN_HOST:-0.0.0.0}" \
        --port "${UVICORN_PORT:-8000}" \
        --proxy-headers \
        --workers "${UVICORN_WORKERS:-2}" \
        --no-access-log
    ;;
*)
    echo "NO ENV SPECIFIED!"
    exit 1
    ;;
esac
