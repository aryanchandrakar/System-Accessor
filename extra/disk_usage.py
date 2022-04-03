import psutil
import time
from subprocess import call

memory_active=1
memory_slab=1
memory_cached=1
diskusage_ini=1
while True:
    #######################################################
    # Clear the screen using a bash command
    call("clear")
    # Disk I/O counts
    print("\n---Disk I/O counts---\n")
    diskio = psutil.disk_io_counters()
    print(diskio)

    time.sleep(1)