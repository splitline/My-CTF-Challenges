#!/bin/bash

git clone https://github.com/wupco/PHP_INCLUDE_TO_SHELL_CHAR_DICT
cd PHP_INCLUDE_TO_SHELL_CHAR_DICT && git apply ../test.py.diff
python test.py
