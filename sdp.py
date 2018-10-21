"""
sdp.py
Session Description Protocol (SDP) file parser.

https://github.com/sam210723/rtsp-debug
"""

import argparse
import base64
from colorama import init as init_color
from colorama import Fore, Back, Style
import tools

# Parse arguments
argparser = argparse.ArgumentParser(description="Session Description Protocol (SDP) file parser.")
argparser.add_argument("path", action="store", help="SDP file path")
args = argparser.parse_args()

print(Style.BRIGHT + "Session Description Protocol (SDP) file parser." + Style.RESET_ALL)
print("http://github.com/sam210723/rtsp-debug\n")

def init(path):
    # Open SDP file
    sdpFile = open(path, mode="r")

    # Parse line-by-line
    for line in sdpFile:
        t = line[0]           # Line type
        v = line[2:].strip()  # Line value

        if (t == "v"):    # Version
            p_v(v)
        elif (t == "o"):  # Origin
            p_o(v)
        elif (t == "s"):  # Session Name
            p_s(v)
        elif (t == "i"):  # Information
            p_i(v)
        elif (t == "u"):  # URI
            p_u(v)
        elif (t == "e"):  # Email address
            p_e(v)
        elif (t == "p"):  # Phone number
            p_p(v)
        elif (t == "c"):  # Connection
            p_c(v)
        elif (t == "b"):  # Bandwidth
            p_b(v)
        elif (t == "t"):  # Timing
            p_t(v)
        elif (t == "r"):  # Repeat
            p_r(v)
        elif (t == "z"):  # Timezone
            p_z(v)
        elif (t == "k"):  # Encryption
            p_k(v)
        elif (t == "a"):  # Attribute
            p_a(v)
        elif (t == "m"):  # Media
            p_m(v)
        else:
            print("Unrecognised type: {}".format(t))
    
        print()  # Newline between types


# Parse functions
def p_v(v):  # Version
    if (v == "0"):
        print("{}SDP Version:    {}0 (RFC4566)".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL))
    else:
        print("{}SDP Version:    {}{}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, v))

def p_o(v):  # Origin
    toks = v.split(" ")

    print(Style.BRIGHT + Fore.GREEN + "Origin:" + Style.RESET_ALL)
    print("{}  - Username:         {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[0]))
    print("{}  - Session ID:       {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
    print("{}  - Session version:  {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[2]))
    
    if (toks[3] == "IN"):
        print("{}  - Network:          {}IN (Internet)".format(Style.BRIGHT, Style.RESET_ALL))
    else:
        print("{}  - Network:          {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[3]))

    if (toks[4] == "IP4"):
        print("{}  - IP version:       {}IPv4".format(Style.BRIGHT, Style.RESET_ALL))
    elif (toks[4] == "IP6"):
        print("{}  - IP version:       {}IPv6".format(Style.BRIGHT, Style.RESET_ALL))
    else:
        print("{}  - IP version:       {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[4]))
    
    print("{}  - Address:          {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[5]))

def p_s(v):  # Session Name
    print("{}Session Name:         {}\"{}\"".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, v))

def p_i(v):  # Information
    print("{}Information:          {}\"{}\"".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, v))

def p_u(v):  # URI
    print("{}URI:                  {}{}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, v))

def p_e(v):  # Email address
    print("{}Email address:        {}{}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, v))

def p_p(v):  # Phone number
    print("{}Phone number:         {}{}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL, v))

def p_c(v):  # Connection
    toks = v.split(" ")

    print(Style.BRIGHT + Fore.GREEN + "Connection:" + Style.RESET_ALL)
    if (toks[0] == "IN"):
        print("{}  - Network:          {}IN (Internet)".format(Style.BRIGHT, Style.RESET_ALL))
    else:
        print("{}  - Network:          {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[0]))

    if (toks[1] == "IP4"):
        print("{}  - IP version:       {}IPv4".format(Style.BRIGHT, Style.RESET_ALL))
    elif (toks[1] == "IP6"):
        print("{}  - IP version:       {}IPv6".format(Style.BRIGHT, Style.RESET_ALL))
    else:
        print("{}  - IP version:       {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
    
    # TTL
    if "/" in toks[2]:
        addrToks = toks[2].split("/")

        # Multiple addresses
        if (len(addrToks) == 3):
            print("{}  - Addresses:        {}".format(Style.BRIGHT, Style.RESET_ALL), end="")

            for i in range(int(addrToks[2])):
                octs = addrToks[0].split(".")
                ip = "{}.{}.{}.{}".format(octs[0], octs[1], octs[2], int(octs[3]) + i)
                print("{} ".format(ip), end="")
            print()
        else:
            print("{}  - Address:          {}{}".format(Style.BRIGHT, Style.RESET_ALL, addrToks[0]))
        
        print("{}  - TTL:              {}{}".format(Style.BRIGHT, Style.RESET_ALL, addrToks[1]))
    else:
        print("{}  - Address:          {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[2]))

def p_b(v):  # Bandwidth
    toks = v.split(":")

    print(Style.BRIGHT + Fore.GREEN + "Bandwidth:" + Style.RESET_ALL, end="")
    if (toks[0] == "CT"):
        print("            CT (Conference Total)", end="")
    elif (toks[0] == "AS"):
        print("            AS (Application Specific)", end="")
    else:
        print("            {}".format(toks[0]), end="")
    
    print(", {} Mbps".format(int(toks[1])/1024))

def p_t(v):  # Timing
    toks = v.split(" ")

    print(Style.BRIGHT + Fore.GREEN + "Timing:" + Style.RESET_ALL)
    print("{}  - Start:            {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[0]))
    print("{}  - Stop:             {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))

def p_r(v):  # Repeat
    toks = v.split(" ")

    print(Style.BRIGHT + Fore.GREEN + "Repeat:" + Style.RESET_ALL)
    print("{}  - Interval:         {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[0]))
    print("{}  - Duration:         {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
    print("{}  - Offsets:          {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[2]), end="")

    # Additional offsets
    for i in range(len(toks)-3):
        print(", " + toks[i+3], end="")
    
    print()

def p_z(v):  # Timezone
    toks = v.strip().split(" ")

    print(Style.BRIGHT + Fore.GREEN + "Timezone:" + Style.RESET_ALL)

    # Loop through adjustment list
    for i in range(int(len(toks)/2)):
        adj = i + 1
        time = toks[i * 2]
        offset = toks[i * 2 + 1]
        print("{}  - Adjustment {}:     {}{} at {}".format(Style.BRIGHT, adj, Style.RESET_ALL, offset, time))

def p_k(v):  # Encryption
    print(Style.BRIGHT + Fore.GREEN + "Encryption:" + Style.RESET_ALL)
    
    if ":" in v:
        toks = v.split(":")
        print("{}  - Method:           {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[0]))

        if (toks[0] == "clear"):
            print("{}  - Key:              {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
        elif (toks[0] == "base64"):
            decoded = base64.decodebytes(bytes(toks[1], encoding="utf-8")).decode("utf-8")
            print("{}  - Key:              {}\"{}\" ({})".format(Style.BRIGHT, Style.RESET_ALL, decoded, toks[1]))
        elif (toks[0] == "uri"):
            print("{}  - URI:              {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
        
    else:
        print("{}  - Method:           {}{}".format(Style.BRIGHT, Style.RESET_ALL, v))

def p_a(v):  # Attribute
    toks = v.split(":")
    attr = toks[0]

    print(Style.BRIGHT + Fore.GREEN + "Attribute:" + Style.RESET_ALL)

    if (attr == "cat"):         # Category
        print("{}  - Type:             {}Session category".format(Style.BRIGHT, Style.RESET_ALL))
        print("{}  - Value:            {}".format(Style.BRIGHT, Style.RESET_ALL), end="")
        cats = toks[1].split(".")

        # Loop through categories and display in cascading tree structure
        i = 0
        for c in cats:
            if i > 0:
                print("\n\t\t       ", end="")

                for j in range(i):
                    print(" ", end="")
                print("└ ", end="")
            print("\"{}\"".format(c), end="")
            i += 1
    elif (attr == "keywds"):    # Keywords
        print("{}  - Type:             {}Session keywords".format(Style.BRIGHT, Style.RESET_ALL))
        print("{}  - Value:            {}".format(Style.BRIGHT, Style.RESET_ALL), end="")
        words = toks[1].split(".")

        i = 0
        for w in words:
            if i > 0:
                print(", ", end="")
            print("\"{}\"".format(w), end="")
            i += 1
    elif (attr == "tool"):      # Tool
        print("{}  - Type:             {}SDP creation tool name".format(Style.BRIGHT, Style.RESET_ALL))
        print("{}  - Value:            {}\"{}\"".format(Style.BRIGHT, Style.RESET_ALL, toks[1]), end="")
    elif (attr == "ptime"):     # Packet time
        print("{}  - Type:             {}Packet time".format(Style.BRIGHT, Style.RESET_ALL))
        print("{}  - Value:            {}{}ms".format(Style.BRIGHT, Style.RESET_ALL, toks[1]), end="")
    elif (attr == "maxptime"):  # Maximum packet time
        print("{}  - Type:             {}Maximum packet time".format(Style.BRIGHT, Style.RESET_ALL))
        print("{}  - Value:            {}{}ms".format(Style.BRIGHT, Style.RESET_ALL, toks[1]), end="")
    elif (attr == "recvonly"):  # Receive only
        print("{}  - Type:             {}Receive-only session".format(Style.BRIGHT, Style.RESET_ALL), end="")
    
    print()


def p_m(v):  # Media
    toks = v.split(" ")

    print(Style.BRIGHT + Fore.GREEN + "Media:" + Style.RESET_ALL)
    print("{}  - Type:             {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[0].title()))

    # Extended protocol name
    if (toks[2] == "RTP/AVP"):
        print("{}  - Protocol:         {}RTP Profile for Audio and Video Conferences (RTP/AVP)".format(Style.BRIGHT, Style.RESET_ALL))
    elif (toks[2] == "RTP/SAVP"):
        print("{}  - Protocol:         {}Secure RTP Profile for Audio and Video Conferences (RTP/SAVP)".format(Style.BRIGHT, Style.RESET_ALL))
    else:
        print("{}  - Protocol:         {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[2].upper()))

    # RTP specific ports and payload formats
    if ("RTP" in toks[2]):
        if "/" in toks[1]:
            portToks = toks[1].split("/")
            rtpPorts = ""
            rtcpPorts = ""
            for i in range(int(portToks[1])):
                rtpPorts += str(int(portToks[0]) + (i * 2)) + " "
                rtcpPorts += str(int(portToks[0]) + (i * 2) + 1) + " "
            
            print("{}  - RTP Ports:        {}{}".format(Style.BRIGHT, Style.RESET_ALL, rtpPorts))
            print("{}  - RTCP Ports:       {}{}".format(Style.BRIGHT, Style.RESET_ALL, rtcpPorts))
        else:
            print("{}  - RTP Port:         {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
            print("{}  - RTPC Port:        {}{}".format(Style.BRIGHT, Style.RESET_ALL, int(toks[1])+1))
        
        # Payload format type
        print("{}  - Format:           {}{}: ".format(Style.BRIGHT, Style.RESET_ALL, toks[3]), end="")
        if (toks[3] == "0"):
            print("PCMU")
        elif (toks[3] == "3"):
            print("Group Speciale Mobile (GSM)")
        elif (toks[3] == "4"):
            print("G723")
        elif (toks[3] == "5"):
            print("DVI4 8k")
        elif (toks[3] == "6"):
            print("DVI4 16k")
        elif (toks[3] == "7"):
            print("LPC")
        elif (toks[3] == "8"):
            print("PCMA")
        elif (toks[3] == "9"):
            print("G722")
        elif (toks[3] == "10"):
            print("L16 2ch")
        elif (toks[3] == "11"):
            print("L16")
        elif (toks[3] == "12"):
            print("QCELP")
        elif (toks[3] == "13"):
            print("CN")
        elif (toks[3] == "14"):
            print("MPA")
        elif (toks[3] == "15"):
            print("G728")
        elif (toks[3] == "16"):
            print("DVI4 11k")
        elif (toks[3] == "17"):
            print("DVI4 22k")
        elif (toks[3] == "18"):
            print("G729")
        elif (toks[3] == "25"):
            print("Sun Microsystems CellB")
        elif (toks[3] == "26"):
            print("JPEG")
        elif (toks[3] == "28"):
            print("nv")
        elif (toks[3] == "31"):
            print("H261")
        elif (toks[3] == "32"):
            print("MPV")
        elif (toks[3] == "33"):
            print("MP2T/MPEG Transport Stream")
        elif (toks[3] == "34"):
            print("H263")
        else:
            print(" ?")
    else:
        # Generic (UDP) port(s) and format(s)
        print("{}  - Port:             {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[1]))
        print("{}  - Format:           {}{}".format(Style.BRIGHT, Style.RESET_ALL, toks[3]))


init_color()
init(args.path)
print()
