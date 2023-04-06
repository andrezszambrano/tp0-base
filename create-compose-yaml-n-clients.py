import sys

number_of_clients = int(sys.argv[1])

f = open("docker-compose-dev.yaml", "w")
f.write('''version: '3.9'
name: tp0
services:
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net
    volumes:  
      - type: bind
        source: ./server/config.ini
        target: /config/config.ini
        read_only: true''')

f.write("\n")

for i in range(1, number_of_clients + 1):
    f.write('''
  client{}:
    container_name: client{}
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID={}
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    volumes:  
      - type: bind
        source: ./client/config.yaml
        target: /config/config.yaml
        read_only: true
    depends_on:
      - server'''.format(i, i, i))
    f.write("\n")

f.write('''
volumes:
  server-config:
    external: false
  client-config:
    external: false

networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24''')
f.write("\n")

f.close()