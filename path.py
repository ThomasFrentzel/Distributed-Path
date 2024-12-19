#!/usr/bin/env python3

from pika import BlockingConnection
from sys import argv
from enum import Enum
import time

if len(argv) < 2:
    print(f"Usage: {argv[0]} <id> [<v1> <v2> ...]")
    exit(1)

State = Enum('State', ['INITIATOR', 'IDLE', 'VISITED', 'OK'])

idx = argv[1]
Nx = argv[2:]

state = State.IDLE
entry = None
initiator = False
unvisited = []
start_time = None

print("My ID =", idx)
print("My neighbors =", Nx)

connection = BlockingConnection()
channel = connection.channel()

channel.queue_declare(queue=idx, auto_delete=True)

def send(msg, dests, channel):
    for dest in dests:
        print(f"Sending '{idx}:{msg}' to {dest}")
        channel.basic_publish(exchange="",
                              routing_key=dest,
                              body=idx + ":" + msg)

def receiving(msg, origin, channel):
    print(f"Message '{msg}' received from {origin}")
    global state, unvisited, entry, initiator, start_time

    time.sleep(1)

    if msg == 'T':
        if state == State.IDLE:
            entry = origin
            unvisited = Nx[:]
            if origin in unvisited:
                unvisited.remove(origin)
            initiator = False
            visit(channel)
        elif state == State.VISITED:
            if origin in unvisited:
                unvisited.remove(origin)
            send('B', [origin], channel)

    elif msg == 'R' or msg == 'B':
        if origin in unvisited:
            unvisited.remove(origin)
        if not unvisited and initiator:
            end_time = time.time()
            print(f"Total time: {(end_time - start_time):.2f} seconds")
        visit(channel)

def spontaneously(msg, channel):
    global state, unvisited, initiator, start_time
    unvisited = Nx[:]
    initiator = True
    state = State.INITIATOR
    print("Initiator!")
    start_time = time.time()
    visit(channel)

def visit(channel):
    global state, unvisited, initiator
    if unvisited:
        next_node = unvisited.pop(0)
        state = State.VISITED
        send('T', [next_node], channel)
    else:
        state = State.OK
        if not initiator:
            send('R', [entry], channel)

def callback(channel, method,  properties, msg):
    m = msg.decode().split(":")
    if len(m) < 2:
        msg = m[0]
        origin = "STARTER"
    else:
        msg = m[1]
        origin = m[0]

    if origin.upper() == "STARTER":
        spontaneously(msg, channel)
    else:
        receiving(msg, origin, channel)

channel.basic_consume(queue=idx,
                      on_message_callback=callback,
                      auto_ack=True)

try:
    print(f"{idx}: Waiting for messages...")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
print("Exiting")