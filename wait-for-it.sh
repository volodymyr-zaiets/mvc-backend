#!/bin/bash

TIMEOUT=30
WAIT_SLEEP=2

host_port="$1"
shift
cmd="$@"

host="${host_port%%:*}"
port="${host_port##*:}"

if [ -z "$host" ] || [ -z "$port" ]; then
  echo "Usage: $0 host:port -- <command>"
  exit 1
fi

wait_for_service() {
  timeout="$TIMEOUT"
  while ! nc -z "$host" "$port"; do
    if [ "$timeout" -le 0 ]; then
      echo "Timeout reached. Service $host:$port is not available."
      exit 1
    fi
    echo "Waiting for $host:$port to become available..."
    sleep "$WAIT_SLEEP"
    timeout=$((timeout - WAIT_SLEEP))
  done
  echo "$host:$port is available!"
}

wait_for_service

exec $cmd
