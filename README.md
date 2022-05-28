# System-Accessor
The Accessor is divided into two components each executing different sets of function in order to determine whether the system has been compromised or under one at the moment. Unlike the usual antiviruses offered from several companies checking for flags in the files or running the file for a short period in a sandbox, which can easily be bypassed by using redundant code, hiding the files, making the file polymorphic etc. Thus, to add to the current methods of accessing the system, the structure has been developed in two components namely Network Accessor and Process Monitor which works to check the system’s symptoms in order to provide better results.
<img src="extra/System_accessor.jpg" width=70%> <img src="extra/System_accessor_2.jpg" width=70%>

A general compromised system symptoms could be any of the following and several other not mentioned here:
* Unexpected fast consumption of disk.
* System running at exceptionally slow speed
* Unexpected connection by your computer to internet.
* New unknown files running
* Unusual traffic in & out of network
* Suspicious activity in admin or privileged account
* Dubious network activities indication brute force
* Spike in file activities
* Unusual port being accessed by some process
* Network activity from strange geographical areas
* System crashing/Interrupts
* Unusual usage time
<hr>

## Implementation

### Required Libraries

Import the required libraries using `pip3 install [library_name]`

Required libraries-
* scapy
* time
* pynput
* threading
* smtplib
* colorama
* pyshark
* geocoder
* psutil
* subprocess
* prettytable

### Running the accessor
1. Open up 3 different terminals and two additional either on the same device or another.
2. Run the netowrk monitor ([network_arpspoof_check.py](network_arpspoof_check.py), [port_ip_check.py](port_ip_check.py)), Process Monitor ([process_monitor_check.py](process_monitor_check.py)) scripts on each of the 3 terminals, using `python3 file_name.py`. Change the interface of the network monitors as per need.
3. Several processes would have started on the port_ip_check and process_monitor_check terminal.
4. On the other 2 terminals run the [keylogger](keylogger.py) and [ARP Spoof](arp_spoof.py) attack, using `python3 file_name.py`. You must add the attacker's email and password in the keylogger file to receive email about the same.
5. Once the attack has started the system accessor terminals would alert the user in red seperate from the usual data to have their attemtion.

### [OUTPUT](https://github.com/aryanchandrakar/System-Accessor/tree/main/OUTPUT)
Based on the attacks and normal process running on your system the differnet output images can be seen [here](https://github.com/aryanchandrakar/System-Accessor/tree/main/OUTPUT).
