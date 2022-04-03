import psutil
import time
from subprocess import call
from colorama import init, Fore, Back, Style
## same as in network_connection.py
procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
pid_list=psutil.pids()
while True:
    # call('clear')
    for process in psutil.pids()[:]:
        try:
            p = psutil.Process(process)
            if p.status() == "running":
                print(
                    str(process),
                    p.name(),
                    p.status(),
                    str(p.cpu_percent()) + "%",
                    p.num_threads()
                )
            if process not in pid_list:
                print(Fore.RED+"[+] Started " + str(process) + " "
                      + psutil.Process(process).name()+""+Style.RESET_ALL)
        except Exception as e:
            pass


    # for key, value in procs.items():
    #     print(key, value)
    time.sleep(2)

# added new
# for key,value in procs.items():
#     if ((value.get('username')) == "system" or (value.get('username')) == "System"
#         or (value.get('username')) == "Admin" or (value.get('username')) == "admin"):
#         print("compromised")
#         break

