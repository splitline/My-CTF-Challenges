#!/bin/sh
printf "$PASSWORD" | htpasswd -i -c htpasswd "$USERNAME"
nginx &
su web -c 'julia main.jl'
