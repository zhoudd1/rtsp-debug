import tools

clientColour = "OKBLUE"
serverColour = "OKGREEN"
debug = False
sdpPath = ""

class RTSP:
    
    def __init__(self, debug, sdpPath):
        self.debug = debug
        self.sdpPath = sdpPath

    """
    Client message handling/parsing functions
    """
    def parse_msgs(self, msgs, conn):
        cmd = [""]
        cseq = -1

        for msg in msgs:
            if self.debug and msg:  # If debug output enabled
                tools.printc("           {0}".format(msg), clientColour)

            if str.startswith(msg, "OPTIONS"):
                cmd = self.parse_options(msg)
            elif str.startswith(msg, "DESCRIBE"):
                cmd = self.parse_describe(msg)
            elif str.startswith(msg, "SETUP"):
                cmd = self.parse_setup(msg)
            elif str.startswith(msg, "CSeq"):
                cseq = self.parse_cseq(msg)
            elif str.startswith(msg, "User-Agent"):
                self.parse_ua(msg)
            elif str.startswith(msg, "Accept"):
                cmd.append(self.parse_accept(msg))
            elif str.startswith(msg, "Transport"):
                self.parse_transport(msg)

        self.build_response(conn, cmd, cseq)

    def parse_options(self, msg):
        path = msg[8:-9]
        tools.printc("[CLIENT]:  Requested OPTIONS for \"{0}\"".format(path), clientColour)
        return ["OPTIONS", path]

    def parse_describe(self, msg):
        path = msg[9:-9]
        tools.printc("[CLIENT]:  Requested DESCRIBE for \"{0}\"".format(path), clientColour)
        return ["DESCRIBE", path]

    def parse_setup(self, msg):
        path = msg[6:-9]
        tools.printc("[CLIENT]:  Requested SETUP for \"{0}\"".format(path), clientColour)
        return ["SETUP", path]

    def parse_cseq(self, msg):
        cseq = int(msg[6:])
        tools.printc("[CLIENT]:  Sequence: {0}".format(cseq), clientColour)
        return cseq

    def parse_ua(self, msg):
        if str.startswith(msg[12:], "LibVLC"):
            tools.printc("[CLIENT]:  Detected VLC", clientColour)

    def parse_accept(self, msg):
        accept = msg.split("/")[1]
        tools.printc("[CLIENT]:  Accepting {0}".format(accept.upper()), clientColour)
        return accept

    def parse_transport(self, msg):
        keys = msg[11:].split(';')
        keys[2] = str.replace(keys[2], "client_port=", "")
        tools.printc("[CLIENT]:  Transport {0} as {1} on ports {2}".format(keys[0], keys[1], keys[2]), clientColour)

    """
    Server response functions
    """
    def build_response(self, conn, cmd, cseq):
        # Build response
        if cmd[0] == "OPTIONS":
            self.send_ack(conn)
            self.send_cseq(conn, cseq)
            self.send_options(conn, cmd)
            conn.send(b'\r\n')
        elif cmd[0] == "DESCRIBE":
            self.send_ack(conn)
            self.send_cseq(conn, cseq)
            self.send_sdp(conn, cmd)
            conn.send(b'\r\n')

        print("")

    def send_ack(self, conn):
        if self.debug:
            tools.printc("           RTSP/1.0 200 OK", serverColour)

        conn.send(b'RTSP/1.0 200 OK\r\n')
        tools.printc("[SERVER]:  Acknowledge", serverColour)

    def send_cseq(self, conn, cseq):
        if self.debug:
            tools.printc("           CSeq: {0}".format(cseq), serverColour)

        conn.send(b'CSeq: ' + bytes(str(cseq), encoding="utf-8") + b'\r\n')
        tools.printc("[SERVER]:  Sequence: {0}".format(cseq), serverColour)

    def send_options(self, conn, cmd):
        if self.debug:
            tools.printc("           Public: DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE", serverColour)

        conn.send(b'Public: DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE\r\n')
        tools.printc("[SERVER]:  Returned OPTIONS (Describe, Setup, Teardown, Play, Pause)", serverColour)

    def send_sdp(self, conn, cmd):
        sdpStr = open(self.sdpPath, "r").read()

        if self.debug:
            tools.printc("\r\n" + sdpStr, serverColour)

        conn.send(b'Content-Type: application/sdp\r\n')
        conn.send(b'Content-Length: ' + bytes(str(len(sdpStr)), encoding="utf-8") + b'\r\n')

        conn.send(b'\r\n' + bytes(sdpStr, encoding="utf-8") + b'\r\n')
        tools.printc("[SERVER]:  Sent SDP", serverColour)
