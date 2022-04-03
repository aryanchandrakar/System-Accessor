# Import the required libraries
import psutil
import time
from subprocess import call
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

class process_monitor():
    def __init__(self):
        self.compare_list = [0]
        self.load_list=[0]
        self.pid_list=psutil.pids()
        self.interupt_list=[0]

    # memory check
    def usage_compare(self,amtused):
        if len(self.compare_list)>5:
            self.compare_list=[self.compare_list[-1]]
            # print(self.compare_list)
        self.compare_list=self.compare_list+[amtused]
        result=all(i < j for i, j in zip(self.compare_list, self.compare_list[1:]))
        return result

    # cpu load check
    def load_compare(self,load):
        if len(self.load_list)>5:
            self.load_list=[self.load_list[-1]]
            # print(self.compare_list)
        self.load_list=self.load_list+[load]
        result=all(i < j for i, j in zip(self.load_list, self.load_list[1:]))
        return result

    # interrupts check
    def interrupt_compare(self, load):
        if len(self.load_list) > 5:
            self.load_list = [self.load_list[-1]]
            # print(self.compare_list)
        self.load_list = self.load_list + [load]
        result = all(i < j for i, j in zip(self.load_list, self.load_list[1:]))
        return result


    # main function
    def monitor(self):
        # Run an infinite loop to constantly monitor the system
        dused=0
        while True:
            # Clear the screen using a bash command
            call('clear')
            print(Back.YELLOW+Fore.BLACK+"==============================Monitor======================================"+Style.RESET_ALL)

            ##########################################################################################
            # Fast disk consumption
            print(Back.WHITE+Fore.BLACK+"!----Memory Check----!"+Style.RESET_ALL)
            memory_table = PrettyTable(["Total", "Used",
                                        "Available", "Percentage"])
            vm = psutil.virtual_memory()
            memory_table.add_row([
                vm.total,
                vm.used,
                vm.available,
                vm.percent
            ])
            dused=abs(int(vm.used)-dused)
            print(memory_table)
            perc=(dused/abs(int(vm.used)))*100
            print(Fore.CYAN+"[-] Percentage change in used memory:" + str(perc)+"%"+Style.RESET_ALL)
            print(Fore.CYAN+"[-] Rate of change in used memory:" +str(dused/60)+" per sec"+Style.RESET_ALL)

            ## Unexpected fast disk consumption
            if self.usage_compare(dused):
                print(Fore.RED+"[!] ALERT! Unusual increase in disk space consumption."+Style.RESET_ALL)
            dused=vm.used

            ############################################################################################
            # Increase in system load
            print(Back.WHITE+Fore.BLACK+"\n!----System Load Check----!"+Style.RESET_ALL)
            load=list(psutil.getloadavg())
            load5=load[1] / psutil.cpu_count() * 100
            print( "[+] System load per CPU in last few seconds:"+str(load5))
            if self.load_compare(load5):
                print(Fore.RED+"[!] ALERT! System Overloading."+Style.RESET_ALL)

            ############################################################################################
            # System crash interrupts
            print("\n!----System Interrupt Check----!"+Style.RESET_ALL)
            intp=psutil.cpu_stats().interrupts
            print("[-] Interrupts occurred:"+str(intp))
            if self.interrupt_compare(intp):
                print(Fore.RED+"[!] ALERT! Too many interrupts occurring, "+
                               "possible crash ahead, check/close suspicious files."+Style.RESET_ALL)


            ############################################################################################
            # Fetch the last 10 processes from available processes
            print(Back.WHITE+Fore.BLACK+"\n!----Processes Check----!"+Style.RESET_ALL)

            process_table = PrettyTable(['PID', 'PNAME', 'STATUS',
                                         'CPU', 'NUM THREADS'])
            running_table = PrettyTable(['PID', 'PNAME', 'STATUS',
                                         'CPU', 'NUM THREADS'])

            for process in psutil.pids()[-10:]:
                try:
                    p = psutil.Process(process)
                    process_table.add_row([
                        str(process),
                        p.name(),
                        p.status(),
                        str(p.cpu_percent()) + "%",
                        p.num_threads()
                    ])
                except Exception as e:
                    pass

            for process in psutil.pids()[:]:
                try:
                    p = psutil.Process(process)
                    if p.status() == "running":
                        running_table.add_row([
                            str(process),
                            p.name(),
                            p.status(),
                            str(p.cpu_percent()) + "%",
                            p.num_threads()
                        ])
                        if process not in self.pid_list:
                            print(Fore.YELLOW+"[+] Started " + str(process)+" "+psutil.Process(process).name()+""+Style.RESET_ALL)
                except Exception as e:
                    pass

            print("---Top 10 Processes---")
            print(process_table)
            print("---running processes---")
            print(running_table)

            ###########################################################################################
            # user check for SSH
            user=psutil.users()
            terminal=[index[1] for index in user]
            name=[index[0] for index in user]
            if ((x for x in terminal)=="pts/0" or (x for x in terminal)=="pts/2") \
                and ((x for x in name) !="root"):
                print(Fore.RED+"[!] ALERT! System Compromised, unknown"+
                               " user found on remote SSH."+Style.RESET_ALL)


            ##########################################################################################
            time.sleep(2)

process_monitor().monitor()
