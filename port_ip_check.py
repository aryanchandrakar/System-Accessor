import sys
import time
import pyshark
from colorama import init, Fore, Back, Style
import requests
import json
import geocoder
import psutil
from subprocess import call

# server port exploit check
vulnerable_port=[587,25,    # smtp mail
                 110,       # POP3 mail
                 143,       # IMAP mail - non_encrypted port
                 22,        # SSH - Secure shell - unauthenticated remote attack
                 20,21,     # FTP - File transfer Protocol
                 69,        # T-FTP - less secure FTP
                 3389,      # Windows terminal server - Remote Desktop
                 389,       # LDAP-Lightweight Directory Access
                 161,       # SNMP-Simple Network management Protocol
                 23,        # Telnet - remote login, un-encrypted text msg
                 194]       # relay chat - comm b/w computer and application on other comp.

def location(addr):
    locationgeo=geocoder.ip(addr)
    request_url = 'https://geolocation-db.com/jsonp/' + addr
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result = json.loads(result)
    if locationgeo.city!=None:
        st=(str(locationgeo.city)+", "+str(locationgeo.state)+", "+str(locationgeo.country)+
              "\nat latitude:"+str(result['latitude'])+"; longitude:"+str(result['longitude']))
        return str(st)
    else:
        return 0

def addr_loc(src_addr,dst_addr):
    loc = location((src_addr))
    if loc != 0:
        print(Fore.WHITE + "[-] Possible location of attacker/server attacked:" + loc)
    else:
        loc = location((dst_addr))
        if loc != 0:
            print(Fore.WHITE + "[-] Possible location of attacker/server attacked:" + loc)
        else:
            print("[!] OOPS! Couldn't find the location!")

def if_check():
    if ("Web" not in (psutil.Process(process).name for process in psutil.pids()[:])) or \
            ("firefox" not in (psutil.Process(process).name for process in psutil.pids()[:])) or \
            ("Content" not in (psutil.Process(process).name for process in psutil.pids()[:])) or \
            ("Extensions" not in (psutil.Process(process).name for process in psutil.pids()[:])):
            # add conditions as per need
        # Can hardcode condition using socket library to fetch process_name but it gives more false positive
        return True
    else:
        return False

def port_chk():
    
    while True:

        capture = pyshark.LiveCapture(interface="eth0")

        print(Fore.BLUE+"--- listening on eth0 ---"+Style.RESET_ALL)

        for packet in capture.sniff_continuously():
            # adjusted output
            try:
                # call('clear')
                # get timestamp
                localtime = time.asctime(time.localtime(time.time()))
                # get packet content
                protocol = packet.transport_layer  # protocol type
                src_addr = packet.ip.src  # source address
                src_port = packet[protocol].srcport  # source port
                dst_addr = packet.ip.dst  # destination address
                dst_port = packet[protocol].dstport  # destination port
                if int(src_port) in vulnerable_port or int(dst_port) in vulnerable_port:

                    # Mail port exploited        ---------------------        ---------------------        ---------------------        ---------------------          
                    if (int(src_port) or int(dst_port)) == (587 or 25 or 110 or 143):
                        # chk=input(Fore.YELLOW+"[!] Did you send of receive any email around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM COMPROMISED!!\n[+]Exploited server email port.\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to close any suspicious files or shutdown and disconnect system from network.")
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))

                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] SMTP mail check"+Style.RESET_ALL)

                    # SSH exploited        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == 22:
                        # chk=input(Fore.YELLOW+"[!] Did you accessed secure shell around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM COMPROMISED!!\n[+]Exploited Secure shell.\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to close any suspicious files or shutdown and disconnect system from network."+Style.RESET_ALL)
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] SSH check"+Style.RESET_ALL)

                    # FTP        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == (20 or 21):
                        chk=input(Fore.YELLOW+"[!] Did you transfer any files to server around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM COMPROMISED!!\n[+]Exploited server file transfer port.\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to shutdown and disconnect system from network."+Style.RESET_ALL)
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] FTP check"+Style.RESET_ALL)

                    # TFTP- Trivial FTP        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == 69:
                        print(Style.BRIGHT + Back.RED + Fore.BLACK + "------------------------------------------------------------------------" + Style.RESET_ALL)
                        print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM MIGHT BE COMPROMISED!!\n[+]Using vulnerable server file transfer port.\n"+Style.RESET_ALL
                                +Fore.CYAN+"Recommended to change network or use different method to transfer files."+Style.RESET_ALL)
                        print(Fore.WHITE + "on %s IP %s:%s <-> %s:%s (%s)" % (
                            localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                        addr_loc(src_addr, dst_addr)
                        print(
                            Style.BRIGHT + Back.RED + Fore.BLACK + "------------------------------------------------------------------------" + Style.RESET_ALL)

                        time.sleep(2)

                    # Windows terminal server or Lightweight Directory Access LDAP exploited        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == (3389 or 389):
                        chk=input(Fore.YELLOW+"[!] Did you transfer control of system/files over network around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM COMPROMISED!!\n[+]Remote desktop/file accessed\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to shutdown and disconnect system from network."+Style.RESET_ALL)
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] LDAP check"+Style.RESET_ALL)

                    # Simple Network management Protocol SNMP exploit        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == (20 or 21):
                        chk=input(Fore.YELLOW+"[!] Did you modify network settings around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            print(Style.BRIGHT+ Fore.RED+"[*] ALERT! NETWORK COMPROMISED!!\n[+]Network settings effected, possible DDoS ahead.\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to shutdown and disconnect system from network."+Style.RESET_ALL)
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] SNMP check"+Style.RESET_ALL)

                    # telnet        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == 23:
                        chk=input(Fore.YELLOW+"[!] Did you contacted any service around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM COMPROMISED!!\n[+]Remote access to network switch.\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to shutdown and disconnect system from network."+Style.RESET_ALL)
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] Telnet check"+Style.RESET_ALL)

                    # relay chat exploit        ---------------------        ---------------------        ---------------------        ---------------------      
                    if (int(src_port) or int(dst_port)) == 194:
                        chk=input(Fore.YELLOW+"[!] Did you send/receive any message to/from other computer's application around "+localtime+"?[Y/N]"+Style.RESET_ALL)
                        if if_check():
                        # if chk=="N"or chk== "n":
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)
                            print(Style.BRIGHT+Fore.RED+"[*] ALERT! SYSTEM COMPROMISED!!\n[+]Root level permission accessed, network overload possible ahead.\n"+Style.RESET_ALL
                                  +Fore.CYAN+"Recommended to shutdown and disconnect system from network."+Style.RESET_ALL)
                            print(Fore.YELLOW + "on %s IP %s:%s <-> %s:%s (%s)" % (
                                localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                            addr_loc(src_addr, dst_addr)
                            print(Style.BRIGHT+ Back.RED+Fore.BLACK+"------------------------------------------------------------------------"+Style.RESET_ALL)

                            time.sleep(2)
                        # elif chk==("Y"or"y"):
                        #     continue
                        else:
                            print(Fore.GREEN+"[+] IRC check"+Style.RESET_ALL)

                else:
                    # output packet info
                    # print(Fore.BLUE+"--- Listening on eth0 ---"+Style.RESET_ALL)
                    print(Fore.WHITE+"%s IP %s:%s <-> %s:%s (%s)" % (localtime, src_addr, src_port, dst_addr, dst_port, protocol))
                # time.sleep(1)
            except AttributeError as e:
                # ignore packets other than TCP, UDP and IPv4
                pass
            print(" ")


call('clear')
port_chk()
