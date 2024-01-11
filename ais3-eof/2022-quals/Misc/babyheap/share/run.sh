#!/bin/sh

# exec 2>/dev/null
export XONSH_DATA_DIR="/tmp/.xondata"
timeout 180 xonsh /home/babyheap/main.xonsh
