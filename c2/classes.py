import socket
import threading
import sys
import time, select
import readline

#Class to manage console messages
class Msg:
    def info(m):
        print("[*] {0:s}".format(str(m)))

    def err(m):
        print("[-] {0:s}".format(str(m)))

    def warn(m):
        print("[!] {0:s}".format(str(m)))

    def ok(m):
        print("[+] {0:s}".format(str(m)))

    def dbg(m):
        print("dbg >>> {0:s}".format(str(m)))

#Auto-completion aid class
class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

#Classes used to interact with the agents
class ConnectionHandler:
    SOCK=socket.socket()
    RHOST=""
    RPORT=""
    CONN=False
    LAG=0
    PROMPT=" "

    def setLAG(self,lag):
        self.LAG=float(lag)
    
    def interact(self):
        readline.parse_and_bind("tab: self-insert")
        try:
            while self.CONN!=False:
                uinput=input(self.PROMPT)+"\n"
                self.SOCK.send(uinput.encode())
                time.sleep(self.LAG)
        except KeyboardInterrupt:
            Msg.info("Returning back to main console")

    def sktRecv(self):
        try:
            while self.CONN:
                data = self.SOCK.recv(1024)
                if not data:
                    Msg.warn("Port: {0:d} Session terminated".format(self.LPORT))
                    self.CONN=False
                    return
                print(str(data.decode(errors='ignore')),end='')
                #print(' ',end='')
                sys.stdout.flush()
        except KeyboardInterrupt:
            return
        except:
            Msg.dbg(threading.currentThread().name)
            Msg.warn("Leaving connection")
            return            

    def sktSend(self, data):
        self.SOCK.send(data.encode())
    
    def disconnect(self):
        Msg.info("Closing connection...")
        self.CONN=False
        try:
            self.SOCK.shutdown(socket.SHUT_RDWR)
            self.SOCK.close()            
        except:
            Msg.warn("Socket already closed!")

class ReverseConnectionHandler(ConnectionHandler):
    LHOST=""
    LPORT=0
    TYPE="plain_rev"

    def __init__(self,lhost,lport):
        self.LHOST="0.0.0.0" # By default listens in all interfaces
        self.LPORT=int(lport)   
    
    def __init__(self,lhost,lport,lag):
        self.LHOST="0.0.0.0" # By default listens in all interfaces
        self.LPORT=int(lport)
        self.LAG=float(lag)

    def connect(self):
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            s.setblocking(1)
            s.settimeout(30)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.LHOST, self.LPORT))
            s.listen(1)
            conn, addr = s.accept()
            Msg.ok("Connected from {0:s}".format(str(addr)))
            self.CONN=True
            self.SOCK=conn
            self.RHOST=addr
            threading.Thread(target=self.sktRecv).start()
            return True
        except KeyboardInterrupt:
            Msg.warn("Connection cancelled")
            return False        
        except:
            Msg.err("Connection Error")
            return False
        
class AgentReverseHandler(ReverseConnectionHandler):
    TYPE="agent_rev"
    