#!/bin/sh

exec 2>/dev/null
SANDBOX=$(mktemp -d /tmp/simp.XXXXXX)
cd $SANDBOX
timeout 30 /home/ctf/chal.py
rm -rf $SANDBOX
