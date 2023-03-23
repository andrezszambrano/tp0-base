#!/bin/bash
echo "hello world" | nc -w 2 server 12345 > auxfile.txt
read -r RESULT < auxfile.txt
[ "hello world" = "${RESULT}" ] && echo “test passed” || echo “test failed”