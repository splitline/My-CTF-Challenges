#!/usr/local/bin/python3
while True:
    mod, attr, value = input('>>> ').split(' ')
    setattr(__import__(mod), attr, value)
