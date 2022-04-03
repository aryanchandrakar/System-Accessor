import psutil
# Iterate over all running process
for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid
        # print(processName , ' ::: ', processID)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
for key, value in procs.items():
    print(key, value)

print("\n")
print("-------------------TCP------------------")
# access network layer info - internet protocol
for i in psutil.net_connections(kind="tcp"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")
print("\n")
print("------------------TCP4-----------------")

for i in psutil.net_connections(kind="tcp4"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")
print("\n")
print("------------------TCP6-------------------")
for i in psutil.net_connections(kind="tcp6"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")

print("\n")
print("------------------UDP------------------")

for i in psutil.net_connections(kind="udp"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")
print("\n")
print("-----------------UDP4-----------------")
for i in psutil.net_connections(kind="udp4"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")
print("\n")
print("-----------------UDP6--------------------")
for i in psutil.net_connections(kind="udp6"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")

print("\n")
print("-------------------INET------------------")

for i in psutil.net_connections(kind="inet"):
    for key,value in procs.items():
        if key==i.pid:
            print(key,value)
    print(i.laddr,i.raddr,i.pid)
    print("\n")

print("\n")



counter=(psutil.net_io_counters(pernic=True))
print(counter.get('eth0'))
