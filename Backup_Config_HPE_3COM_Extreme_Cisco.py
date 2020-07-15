#--------------LIBRARY------------------------
import telnetlib
import os
import sys
import time
from datetime import date
import shutil
import pyAesCrypt
#--------------END OF LIBRARY------------------------


#--------------USER VARIABLE------------------------
bufferSize = 64 * 1024
tftp="IP_ADDRRESS"
ip=[]
login=[]
password=[]
switch_os=[]
counter=0
#--------------END OF USER VARIABLE------------------------


#--------------MAKE NEW DIRECTORY------------------------
newpath = r"PATH" + str(date.today())
if not os.path.exists(newpath):
    os.makedirs(newpath)
#--------------END OF MAKE NEW DIRECTORY------------------


#--------------DECODE BASE ------------------------
main_password = input("Password: ")
pyAesCrypt.encryptFile(r"PATH", r"PATH", main_password, bufferSize)
pyAesCrypt.decryptFile(r"PATH", r"PATH", main_password, bufferSize)
file = open(r"PATH_TO_DEVICE_LIST","r")

for line in file:
    x=line.split(",")
    ip.append(x[0])
    login.append(x[1])
    password.append(x[2])
    switch_os.append(x[3])
    counter=counter+1
file.close()
#--------------END OF DECODE BASE ------------------------

for j in range (counter):

    # --------------GET CONFIG HP------------------------------------------
    if switch_os[j]=="HP_OS":
        tn = telnetlib.Telnet(ip[j])
        time.sleep(1)
        tn.write(b"\n")
        tn.read_until(b"Username:")
        tn.write(login[j].encode('ascii') + b"\n")
        tn.read_until(b"Password:")
        tn.write(password[j].encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(b"conf t\n")
        time.sleep(1)
        tn.write(b"copy running-config tftp " + tftp.encode('ascii') + b" config-" + ip[j].encode('ascii') + b"\n")
        time.sleep(30)
        print ("Done\n")
    # --------------END OF GET CONFIG HP------------------------------------------

    # --------------GET CONFIG 3_COM------------------------------------------
    if switch_os[j] == "3_COM":
        tn = telnetlib.Telnet(ip[j])
        time.sleep(1)
        tn.read_until(b"Login:")
        tn.write(login[j].encode('ascii') + b"\r\n")
        time.sleep(0)
        tn.read_until(b"Password:")
        tn.write(password[j].encode('ascii') + b"\r\n")
        time.sleep(1)
        tn.write(b"system backupConfig save\r\n")
        time.sleep(1)
        tn.write(tftp.encode('ascii') + b"\r\n")
        time.sleep(1)
        tn.write(b"config-" + ip[j].encode('ascii') + b"\r\n")
        time.sleep(1)
        tn.write(b"\r\n")
        time.sleep(180)
        print("Done\n")
    # --------------END OF GET CONFIG 3_COM------------------------------------------

    # --------------GET CONFIG CISCO------------------------------------------
    if switch_os[j] == "CISCO_OS":
        tn = telnetlib.Telnet(ip[j])
        time.sleep(1)
        tn.read_until(b"Password:")
        tn.write(password[j].encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(b"enable" + b"\n")
        time.sleep(1)
        tn.write(password[j].encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(b"copy running-config tftp: " + b"\n")
        time.sleep(1)
        tn.write(tftp.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(b" config-" + ip[j].encode('ascii') + b"\n")
        time.sleep(30)
        print("Done\n")
    # --------------END OF GET CONFIG CISCO------------------------------------------

    '''
    # --------------GET CONFIG EXTREME------------------------------------------
    

    if switch_os[j] == "EXOS":   
        tn = telnetlib.Telnet(host)
        time.sleep(1)
        tn.read_until(b"login:")
        tn.write(user.encode('ascii') + b"\n")
        tn.read_until(b"password:")
        tn.write(password.encode('ascii') + b"\n")
        time.sleep(1)
        tn.write(b"tftp put " + tftp.encode('ascii') +  b" primary.cfg config-" + host.encode('ascii') +b"\n")
        time.sleep(30)
        print ("Done\n")
    '''
    # --------------END OF GET CONFIG EXTREME------------------------------------------


    #--------------MOVE CONFIG TO DATE_FOLDER------------------------------------------
    tftp_dir=r"PATH"
    save_dir=r"PATH"
    os.replace(tftp_dir+"config-"+str(ip[j]), save_dir+"_"+str(date.today())+"/_"+"config-"+str(ip[j]))
    #--------------END OF MOVE CONFIG TO DATE_FOLDER------------------------------------------


#--------------ENCODE BASE AND REMOVE DECONDE FILE ------------------------
pyAesCrypt.encryptFile(r"PATH", r"PATH", main_password, bufferSize)  #encrypt device database
os.remove(r"PATH")     #erease database file
#--------------END OF ENCODE BASE AND REMOVE DECONDE FILE ------------------------


print ("Done")

