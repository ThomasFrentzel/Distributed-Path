#!/usr/bin/env python3

from pika import BlockingConnection
from sys import argv

if len(argv) < 3:
    print(f"Usage: {argv[0]} <message> <dest1> [<dest2> ...]")
    exit(1)

message = argv[1]
destinations = argv[2:]

def send(msg, dest, channel):
    channel.basic_publish(exchange="",
                          routing_key=dest,
                          body="STARTER:" + msg)

connection = BlockingConnection()
channel = connection.channel()

for d in destinations:
    channel.queue_declare(queue=d, auto_delete=True)
    send(message, d, channel)
    print(f'Message "{message}" sent to {d}')

connection.close()
