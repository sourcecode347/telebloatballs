# !/usr/bin/python3
# -*- coding: utf-8    -*-
'''
https://github.com/sourcecode347/telebloatballs/

MIT License

Copyright (c) 2021 Nikolaos Bazigos

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
#################################################################################
# REQUIREMENTS
#################################################################################
# pip3 install termcolor
# pip3 install pyserial
# sudo apt install modemmanager * On Windows Use Manual Port -p COM1
# If you are in Windows uncomment colorama importing and init and run
# pip install colorama
# python telebloatballs.py --help
#################################################################################
# https://www.freedesktop.org/wiki/Software/ModemManager/SupportedDevices/
#################################################################################
# https://en.wikipedia.org/wiki/Telephone_numbers_in_Greece
#################################################################################
# http://patorjk.com/software/taag/#p=display&h=0&v=0&f=Contessa&t=TeleBloatBalls
#################################################################################
logo='''
.___.   .   .__ .       , .__    ..   
  |   _ | _ [__)| _  _.-+-[__) _.|| __
  |  (/,|(/,[__)|(_)(_] | [__)(_]||_)  v 20.01

Coded By Nikolaos Bazigos
'''
print(logo)
import subprocess,os,serial,sys,time,datetime,random
from termcolor import colored
#import colorama
#colorama.init()
r_args=['-m','-a','-d','-p','-h','-s','-n','-o','-c','-help']
global missed,advanced,clearsms,manualport,enablesms,msg,enablestartsnum,outfile,cc,sendfile,smscount,smsmax
sendfile="sbsend.txt"
smscount=0
smsmax=1450
missed=False
advanced=False
clearsms=False
manualport=False
enablesms=False
enablestartsnum=False
outfile="mobiles.txt"
if os.path.exists(outfile)==False:
    f = open(outfile, "a")
    f.close()
msg=""
cc="+30"
for arg in range(0,len(sys.argv)):
    if  "-" in sys.argv[arg] and sys.argv[arg] not in r_args:
        print("run 'sudo python3 telebloatballs.py -help' in terminal ...")
        break
    if sys.argv[arg-1]=="-m":
        missed=True
    if sys.argv[arg-1]=="-a":
        advanced=True
    if sys.argv[arg-1]=="-d":
        clearsms=True
    if sys.argv[arg-1]=="-s":
        msg=sys.argv[arg]
        enablesms=True
    if sys.argv[arg-1]=="-o":
        outfile=sys.argv[arg]
        if os.path.exists(outfile)==False:
            f = open(outfile, "a")
            f.close()
    if sys.argv[arg-1]=="-c":
        cc=sys.argv[arg]
    if sys.argv[arg-1]=="-n":
        numstarts=sys.argv[arg].split(',')
        enablestartsnum=True
    if sys.argv[arg-1]=="-p":
        port=sys.argv[arg]
        manualport=True
    if sys.argv[arg]=="-help" or sys.argv[arg]=="-h":
        print("sudo python3 telebloatballs.py -a -m")
        print(" -a : Include Outgoing Advanced Call")
        print(" -m : Include Outgoing Missed Call")
        print(" -d : Clear SMS On Begin")
        print(" -s : Send SMS -s 'This is a message' * Only Support English Characters In SMS ")
        print(" -p : Modem Port -p /dev/ttyUSB2 ")
        print(" -n : Mobile Number Start -n 693,699 * Supports length 2 to 5 for each value")
        print(" -o : Output File -o windmobiles.txt * Default file is mobiles.txt")
        print(" -c : Country Code -c +30 * Default +30")
def modemport():
    fmodem=str(subprocess.check_output("sudo mmcli -L", shell=True)).strip()
    #print (fmodem)
    fcut1="/org/freedesktop/ModemManager1/Modem/"
    pos1=fmodem.find(fcut1)
    pos1+=len(fcut1)
    nmodem=""
    while fmodem[pos1]!=" ":
        nmodem+=fmodem[pos1]
        pos1+=1
    primaryport='|      primary port:'
    #print(nmodem)
    fport=subprocess.check_output("sudo mmcli -m "+nmodem+" | grep '"+primaryport+"'", shell=True).decode("utf-8")
    enable=subprocess.check_output("sudo mmcli -m "+nmodem+" -e", shell=True).decode("utf-8")
    fport='/dev/'+(fport.replace(primaryport,'').replace(' ','').replace("'",'')).strip()
    return fport
if manualport==False:
    port=modemport() 
ser = serial.Serial(port,baudrate=9600,timeout=0.05)
if enablestartsnum==False:
    numstarts=["693"]
snums=['0','1','2','3','4','5','6','7','8','9']
def randomnum():
    rnum=numstarts[random.randint(0,len(numstarts)-1)]
    if len(rnum)==2:
        rint=8
    if len(rnum)==3:
        rint=7
    if len(rnum)==4:
        rint=6
    if len(rnum)==5:
        rint=5
    for x in range(0,rint):
        rnum+=snums[random.randint(0,len(snums)-1)]
    return rnum
def checkstarts(mbl):
    for x in numstarts:
        if mbl.startswith(x):
            return True
    return False
def advancedcall(mobile):
    g=False
    ser.write('ATZ\r'.encode())
    ser.write(('ATD '+mobile+';\r').encode())
    tnow = datetime.datetime.now()
    current_time = tnow.strftime("%H:%M:%S")
    print("["+colored(current_time,"blue")+"] "+colored("Advanced Call To : ","green",attrs=['bold'])+mobile)
    time.sleep(5)
    counter=0
    sbool=True
    while True:
        try:
            ser.write('AT+CLCC\r'.encode())
            data=ser.read(1024)
            data+= ser.read(ser.inWaiting())
            #print(data)
            f="+CLCC: 1,0,"
            if f in data.decode():
                ddata=data.decode()
                g=ddata[ddata.find(f)+len(f)]
                if sbool==True:
                    print("Status : "+g)
                    sbool=False
                if g=="0" or "+CLCC: 1,0,0" in ddata:
                    break
            if "1,0,0" in data.decode():
                g="0"
                break
            counter+=1
            if counter==100:
                break
            time.sleep(0.1)
        except:
            pass
    ser.write('ATZ\r'.encode())
    ser.write('AT+CHUP\r'.encode())
    time.sleep(1)
    if g=="0":
        tnow = datetime.datetime.now()
        current_time = tnow.strftime("%H:%M:%S")
        print("["+colored(current_time,"blue")+"] "+colored("Detected Number : ", 'red',attrs=['bold'])+mobile)
        if checkstarts(mobile)==True:
            if mobile not in open(outfile).read():
                with open(outfile, "a") as myfile:
                    myfile.write(mobile+"\r\n")
def missedcall(mobile):
    ser.write('ATZ\r'.encode())
    ser.write(('ATD '+mobile+';\r').encode())
    tnow = datetime.datetime.now()
    current_time = tnow.strftime("%H:%M:%S")
    print("["+colored(current_time,"blue")+"] "+colored("Missed Call To : ","green",attrs=['bold'])+mobile)
    time.sleep(5)
    ser.write('ATZ\r'.encode())
    ser.write('AT+CHUP\r'.encode())
    time.sleep(1)
def randnumber():
    while True:
        with open(outfile) as f:
            lines = f.readlines()
        #print(lines[random.randint(0,len(lines)-1)].replace("\r","").replace("\n",""))
        number=cc+lines[random.randint(0,len(lines)-1)].replace("\r","").replace("\n","")
        if number not in open(sendfile).read():
            with open(sendfile, "a") as myfile:
                myfile.write(number+"\r\n")
            break
    return number
def sendsms(msg):
    number=randnumber()
    ser.write('AT+CMGF=1\r'.encode())
    time.sleep(1)
    ser.write('AT+CSCS="GSM"\r'.encode())
    time.sleep(1)
    ser.write(('AT+CMGS="'+number+'"\r').encode())
    time.sleep(1)
    ser.write((msg+chr(26)+'"\r').encode())
    tnow = datetime.datetime.now()
    current_time = tnow.strftime("%H:%M:%S")
    print("["+colored(current_time,"blue")+"] "+colored("Send SMS To : ","grey",attrs=['bold'])+number)
def listlen():
    if os.path.exists(outfile):
        with open(outfile) as f:
            lines = f.readlines()
            print(colored(str(len(lines))+" active mobile numbers in "+outfile,"blue",attrs=['bold']))
delcounter=1
delbool=True
detnumbers=[]
now=datetime.datetime.now()
now = now + datetime.timedelta(0,10)
if missed==False and advanced==False and enablesms==False:
    print(colored("Only Detecting Incoming Calls And SMS","red",attrs=['bold']))
    print(" sudo python3 telebloatballs.py -h ")
else:
    print(colored("Detecting Incoming Calls And SMS","blue",attrs=['bold']))
if advanced==True:
    print(colored("Outgoing Advanced Calls","blue",attrs=['bold']))
if missed==True:
    print(colored("Outgoing Missed Calls","blue",attrs=['bold']))
if enablesms==True:
    print(colored("Sending SMS","blue",attrs=['bold']))
listlen()
while True:
    if now < datetime.datetime.now():
        delcounter+=1
        delbool=True
        if advanced==True:
            advancedcall(randomnum())
        if missed==True:
            missedcall(randomnum())
        if enablesms==True:
            #with open(outfile) as f:
                #lines = f.readlines()
            #print(lines[random.randint(0,len(lines)-1)].replace("\r","").replace("\n",""))
            #number=cc+lines[random.randint(0,len(lines)-1)].replace("\r","").replace("\n","")
            sendsms(msg)#Only Support English Language
            smscount+=1
            print(colored("SMS Count : ","green",attrs=['bold'])+str(smscount))
        now=datetime.datetime.now()
        now=now+datetime.timedelta(0,3)
    if missed==True or advanced==True:
        try:
            ser.write('AT+CPMS="ME","ME","ME"\r'.encode())
            ser.write('AT+CMGF=1\r'.encode())
            #ser.write('AT+CSCS=?\r'.encode())
            rand=random.randint(0,1)
            #rand=2
            if rand==0:
                ser.write('AT+CMGL="ALL"\r'.encode())
            if rand==1:
                ser.write('AT+CMGL="REC UNREAD"\r'.encode())
            if (delcounter%15==0 or clearsms==True) and delbool==True:
                ser.write('AT+CPMS="ME","ME","ME"\r'.encode())
                time.sleep(3)
                ser.write('AT+CMGD=1,4"\r'.encode())
                print(colored("DELETE ALL SMS","yellow",attrs=['bold']))
                delbool=False
                clearsms=False
                listlen()
            data = ser.read(1024)
            data+= ser.read(ser.inWaiting())
            #if data.decode()!="":
                #print (data)
            mdata=data.decode()
            mdata2=data.decode()
            mfind='"REC READ",'
            mfend='",,"'
            mnumbers=[]
            while mfind in mdata:
                mpos=mdata.find(mfind)+len(mfind)
                mpend=mdata.find(mfend)
                mnum=mdata[mpos:mpend]
                rep=mfind+mnum+mfend
                mnum=mnum.replace('"'+cc.replace("+",""),"").replace(cc,"")
                if len(mnum)!=10:
                    break
                if mnum not in detnumbers:
                    tnow = datetime.datetime.now()
                    current_time = tnow.strftime("%H:%M:%S")
                    print("["+colored(current_time,"blue")+"] "+colored("Detected Number : ", 'red',attrs=['bold'])+mnum)
                    mnumbers.append(mnum)
                    detnumbers.append(mnum)
                mdata=mdata.replace(rep,"")
            if len(mnumbers)>0:
                for x in mnumbers:
                    if checkstarts(x)==True:
                        if    x not in open(outfile).read():
                            with open(outfile, "a") as myfile:
                                myfile.write(x+"\r\n")
            mdata=mdata2
            mfind='"REC UNREAD",'
            mfend='",,"'
            mnumbers=[]
            while mfind in mdata:
                mpos=mdata.find(mfind)+len(mfind)
                mpend=mdata.find(mfend)
                mnum=mdata[mpos:mpend]
                rep=mfind+mnum+mfend
                mnum=mnum.replace('"'+cc.replace("+",""),"").replace(cc,"")
                if len(mnum)!=10:
                    break
                if mnum not in detnumbers:
                    tnow = datetime.datetime.now()
                    current_time = tnow.strftime("%H:%M:%S")
                    print("["+colored(current_time,"blue")+"] "+colored("Detected Number : ", 'red',attrs=['bold'])+mnum)
                    mnumbers.append(mnum)
                    detnumbers.append(mnum)
                mdata=mdata.replace(rep,"")
            if len(mnumbers)>0:
                for x in mnumbers:
                    if checkstarts(x)==True:
                        if x not in open(outfile).read():
                            with open(outfile, "a") as myfile:
                                myfile.write(x+"\r\n")
            #if "CLIP" in data.decode() or "RING" in data.decode() or "LIP" in data.decode():
            if 'IP: "' in data.decode():
                phonenumber="Uknown"
                if 'IP: "' in data.decode():
                    decdata=data.decode()
                    pos=decdata.find('IP: "')+len('IP: "')
                    phonenumber=""
                    while decdata[pos]!='"':
                        phonenumber+=decdata[pos]
                        pos+=1
                tnow = datetime.datetime.now()
                current_time = tnow.strftime("%H:%M:%S")
                print ("["+colored(current_time,"blue")+"] "+colored("Incoming Call From : ", 'blue',attrs=['bold'])+phonenumber.replace(cc,""))
                phonenumber=phonenumber.replace(cc,"")
                if (phonenumber!="Uknown") and checkstarts(phonenumber)==True:
                    print (phonenumber+colored(" Call You",'blue'))
                    if phonenumber not in open(outfile).read():
                        with open(outfile, "a") as myfile:
                            myfile.write(phonenumber+"\r\n")
                #Close the Phone
                ser.write('ATZ\r'.encode())
                time.sleep(1)
                ser.write('AT+CHUP\r'.encode())
                time.sleep(1)
        except:
            pass
