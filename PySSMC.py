#
# -=-=-=-=- PySSMC v0.0.1 -=-=-=-=-
# Author: Bar Tselenchuk
# Source Code: https://github.com/bartselen/PySSMC/
#
# LICENSE:
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.
#

import socket
import ssl
import base64
import getpass
import sys
import getopt

SERVERIP = "smtp.gmail.com"
PORT = 25

USERNAME = "bartselen@gmail.com"
PASSWORD = "gamecenter1"
RCPTLIST = []
_verbose = 0
MSGSUBJECT = "Get Ready!"
MSGCONTENT = "Frusta was here"
def usage():
    print "Usage: pyssmc.py [-v || --verbose]"
scc = None

print "PySSMC Client v0.0.1"
def main(argv):
    global USERNAME
    global PASSWORD
    global RCPTLIST
    global MSGSUBJECT
    global MSGCONTENT
    global scc
    
    try:                                
        opts, args = getopt.getopt(argv, "v", ["verbose"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
            global _verbose
            _verbose = 1
        else:
            print "fuck"

    USERNAME = raw_input("Enter email address: ")
    PASSWORD = getpass.getpass()

    AUTH = False
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to " + SERVERIP + " on port " + str(PORT)
    cSocket.connect((SERVERIP, PORT))

    recv = cSocket.recv(1024)
    if _verbose == 1:
        print "<< " + recv
    cSocket.send("EHLO\r\n")
    if _verbose == 1:
        print ">> EHLO\r\n"
	
    recv = cSocket.recv(1024)
    if _verbose == 1:
        print "<< " + recv
    command = "STARTTLS\r\n"
    cSocket.send(command)
    if _verbose == 1:
        print ">> STARTLS\r\n"
    recv = cSocket.recv(1024)
    if _verbose == 1:
        print "<< " + recv
    scc = ssl.wrap_socket(cSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    scc.send('auth login\r\n')
    if _verbose == 1:
        print ">> auth login\r\n"
    recv = scc.recv(1024)
    if _verbose == 1:
        print "<< " + recv
    scc.send(base64.b64encode(USERNAME)+'\r\n')
    if _verbose == 1:
        print ">> " + base64.b64encode(USERNAME)+'\r\n'
    recv = scc.recv(1024)
    if _verbose == 1:
        print "<< " + recv
    scc.send(base64.b64encode(PASSWORD)+'\r\n')
    if _verbose == 1:
        print ">> " + base64.b64encode(PASSWORD)+'\r\n'
    recv = scc.recv(1024)
    if _verbose == 1:
        print "<< " + recv
	
    print "Login successful"
    while True:
        scc.send("MAIL FROM:<"+USERNAME+">\r\n")
        if _verbose == 1:
            print ">> MAIL FROM:<"+USERNAME+">\r\n"
        recv = scc.recv(1024)
        if _verbose == 1:
            print "<< " + recv
        break
		
    RECPT = raw_input("Enter recipient list terminated by -1")
    RCPTLIST.append(RECPT)
    while RECPT != "-1":
        RECPT = raw_input("Enter recipient: ")
        if RECPT != "-1":
            RCPTLIST.append(RECPT)

    for mail in RCPTLIST:
        while True:
            scc.send("RCPT TO:<"+mail+">\r\n")
            if _verbose == 1:
                print ">> RCPT TO:<"+mail+">\r\n"
            recv = scc.recv(1024)
            if _verbose == 1:
                print "<< " + recv
            if "250 2.1.5 OK" in recv:
                break

			   
    MSGSUBJECT = raw_input("Message subject: ")
    MSGCONTENT = raw_input("Message content: ")

    while True:
        scc.send("DATA\r\n")
        if _verbose == 1:
            print ">> DATA\r\n"
        recv = scc.recv(1024)
        if _verbose == 1:
            print "<< " + recv
        if "354" in recv and "Go ahead" in recv:
            break

    while True:
        scc.send("Subject: " + MSGSUBJECT + "\r\n"+ MSGCONTENT + "\r\n.\r\n")
        if _verbose == 1:
            print ">> Subject: " + MSGSUBJECT + "\r\n"+ MSGCONTENT + "\r\n.\r\n"
        recv = scc.recv(1024)
        if _verbose == 1:
            print "<< " + recv
        if "250" in recv:
            break
        else:
            if _verbose == 1:
                print recv
    print "Email has been sent!"
    while True:
        scc.send("QUIT")
        if _verbose == 1:
            print ">> QUIT"
        recv = scc.recv(1024)
        if _verbose == 1:
            print "<< " + recv
        if "221 2.0.0" in recv:
            break
    if _verbose == 1:
        print recv
    input()
    print "Closing connection."
    scc.close()
    cSocket.close()

    
if __name__ == "__main__":
    main(sys.argv[1:])
