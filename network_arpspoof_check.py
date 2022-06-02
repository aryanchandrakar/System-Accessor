import sys

import scapy.all as scapy
from colorama import init, Fore, Back, Style

# RUN ARP SPOOFER FOR EXTERNAL WIFI NETWORK ATTACKS !!!!

def get_mac(ip):
    # dicovering client thru mac request who has which mac
    arp_request=scapy.ARP(pdst=ip)
    # the mac of the address we arp request ff:ff:ff....
    broadcast= scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # discover hosts on a network
    arp_request_broadcast= broadcast/arp_request
    # to get the field that can be edited
    answerlist=scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answerlist[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2:
        # check for arp layer and is it of type "is at", relation between mac and ip
        try:
            real_mac=get_mac(packet[scapy.ARP].psrc) # fetch MAC from IP(psrc)
            response_mac=packet[scapy.ARP].hwsrc # hwsrc - fetch Mac corresponding to psrc
            if real_mac != response_mac:
                print(Fore.RED+"[~] You are under attack! Check your network")
                sys.exit(Fore.GREEN+"Get to Safety!")
        # print(packet.show())
        except IndexError:
            pass

sniff("eth0")
