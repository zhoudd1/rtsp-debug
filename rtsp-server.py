"""
rtsp-server.py

https://github.com/sam210723/rtsp-debug
"""

import argparse
import socket
import tools

argparser = argparse.ArgumentParser(description="")
argparser.add_argument("-a", action="store", help="RSTP listen interface", default="127.0.0.1")
argparser.add_argument("-p", action="store", help="RSTP listen port", default=554)
argparser.add_argument("-d", action="store_true", help="Enable debug output", default=False)
args = argparser.parse_args()

tools.printc("RTSP Server v0.1", "OKGREEN")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_addr = (args.a, args.p)
try:
    sock.bind(sock_addr)
except:
    tools.printc("Failed to bind socket", "FAIL")
    exit(1)
sock.listen(1)
print("Listening: {0}:{1}\n------------------------------\n".format(args.a, args.p))

while True:
    conn, client = sock.accept()

    try:
        tools.printc("{0} connected".format(client[0]), "BOLD")

        packet = ""
        while True:
            data = conn.recv(1024)
            msgs = data.decode("utf-8").split('\r\n')

            for msg in msgs:
                if msg and args.d:  # If message not null
                    tools.printc("[CLIENT]:  {0}".format(msg), "OKBLUE")

    finally:
        conn.close()
