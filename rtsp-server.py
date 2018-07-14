"""
rtsp-server.py v0.1

https://github.com/sam210723/rtsp-debug
"""

import argparse
import socket
import tools

# Globals
ver = "0.1"
clientColour = "OKBLUE"
serverColour = "OKGREEN"

# Parse arguments
argparser = argparse.ArgumentParser(description="")
argparser.add_argument("-a", action="store", help="RSTP listen interface", default="127.0.0.1")
argparser.add_argument("-p", action="store", help="RSTP listen port", default=554)
argparser.add_argument("-d", action="store_true", help="Enable debug output", default=False)
args = argparser.parse_args()

tools.printc("RTSP Server v{0}".format(ver), "OKGREEN")

# Configure socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_addr = (args.a, args.p)

try:
    sock.bind(sock_addr)
except:
    tools.printc("Failed to bind socket", "FAIL")
    exit(1)


# Begin listening for incoming connections
def listen():
    sock.listen(1)
    print("Listening: {0}:{1}\n------------------------------\n".format(args.a, args.p))

    # Listen forever
    while True:
        conn, client = sock.accept()

        try:
            # Announce new connection
            tools.printc("{0} connected".format(client[0]), "BOLD")

            # Receive forever
            while True:
                data = conn.recv(1024)
                msgs = data.decode("utf-8").split('\r\n')

                for msg in msgs:
                    if msg:  # If message not null
                        if args.d:  # If debug output enabled
                            tools.printc("[DEBUG ]:  {0}".format(msg), clientColour)

                        parse_msg(msg, conn)
        finally:
            conn.close()


# Parse incoming messages
def parse_msg(msg, conn):
    # OPTIONS
    if str.startswith(msg, "OPTIONS"):
        tools.printc("[CLIENT]:  Requested OPTIONS", clientColour)


# Open socket and listen
listen()
