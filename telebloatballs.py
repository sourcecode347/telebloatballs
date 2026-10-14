# !/usr/bin/python3
# -*- coding: utf-8	-*-
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
# pip3 install colorama
# sudo apt install modemmanager
# sudo apt install modem-manager-gui
# Run modem-manager-gui & Enable modem & Execute telebloatballs.py as sudo
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
  |  (/,|(/,[__)|(_)(_] | [__)(_]||_)  v 26.10

Coded By Nikolaos Bazigos
'''
print(logo)
import subprocess,os,serial,sys,time,datetime,random,re
from termcolor import colored
import colorama
colorama.init()
r_args=['-m','-a','-d','-p','-h','-s','-n','-o','-c','--onlydetect','--help']
global missed,advanced,clearsms,manualport,enablesms,enablestartsnum,outfile,cc,sendfile,smscount,smslist,onlydetect,missedcounter,port
sendfile="send.txt"
smscount=0
missed=False
missedcounter=1
advanced=False
clearsms=False
manualport=False
enablesms=False
enablestartsnum=False
outfile="mobiles.txt"
smslist="smslist.txt"
onlydetect=False
port=False
if os.path.exists(outfile)==False:
	f = open(outfile, "a")
	f.close()
cc="+30"
for	arg	in range(0,len(sys.argv)):
	if	"-"	in sys.argv[arg] and sys.argv[arg] not in r_args:
		print("run 'sudo python3 telebloatballs.py --help' in terminal ...")
		break
	if	sys.argv[arg-1]=="-m":
		missedcounter=int(sys.argv[arg])
		missed=True
	if	sys.argv[arg-1]=="-a":
		advanced=True
	if	sys.argv[arg-1]=="-d":
		clearsms=True
	if	sys.argv[arg-1]=="-s":
		smslist=sys.argv[arg]
		enablesms=True
	if	sys.argv[arg-1]=="-o":
		outfile=sys.argv[arg]
		if os.path.exists(outfile)==False:
			f = open(outfile, "a")
			f.close()
	if	sys.argv[arg-1]=="-c":
		cc=sys.argv[arg]
	if	sys.argv[arg-1]=="-n":
		numstarts=sys.argv[arg].split(',')
		enablestartsnum=True
	if	sys.argv[arg-1]=="-p":
		port=sys.argv[arg]
		manualport=True
	if	sys.argv[arg-1]=="--onlydetect":
		onlydetect=True
	if	sys.argv[arg]=="--help" or sys.argv[arg]=="-h":
		print("sudo python3 telebloatballs.py -a -m 5 -n 693,694,697 -p /dev/ttyUSB2")
		print(" -a : Include Outgoing Advanced Call")
		print(" -m : Include Outgoing Missed Call with counter EX. -m 5")
		print(" -d : Clear SMS On Begin")
		print(" -s : Send SMS -s smslist.txt")
		print(" -p : Modem Port -p /dev/ttyUSB2 ")
		print(" -n : Mobile Number Start -n 693,699 * Supports length 2 to 5 for each value")
		print(" -o : Output File -o windmobiles.txt * Default file is mobiles.txt")
		print(" -c : Country Code -c +30 * Default +30")
		print(" --onlydetect : Only Detection - Not Sending SMS On Detection")
if port!=False:
	try:
		ser	= serial.Serial(port,baudrate=9600,timeout=0.05)
	except:
		print("Please Set The Correct Port Of GSM Modem (!)")
		sys.exit()
else:
	print("Please Set The Correct Port Of GSM Modem (!)")
	sys.exit()
if enablestartsnum==False:
	numstarts = ["690","691","693","694","695","697","698","699",]
snums=['0','1','2','3','4','5','6','7','8','9']
def	randomnum():
	while True:
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
		if str(rnum) not in open(outfile).read():
			break
	return	rnum
def checkstarts(mbl):
	for x in numstarts:
		if mbl.startswith(x):
			return True
	return False
def normalize_number(number: str) -> str:
    cleaned = re.sub(r'\D', '', number.strip())
    return cleaned if cleaned else ""
def	snapsms(number,outfile=outfile):
	if number in open(outfile).read():
		return False
	if cc!="+30":
		number=cc+number
	messages = ["SMS Message 1" \
	,"SMS Message 2" \
	,"SMS Message 3" \
	,"SMS Message 4" \
	,"SMS Message 5"]
	msg = messages[random.randint(0,len(messages)-1)]
	msg = msg+" - SMS Message PostFix"
	ser.write('AT+CMGF=1\r'.encode())
	time.sleep(1)
	ser.write('AT+CSCS="GSM"\r'.encode())
	time.sleep(1)
	ser.write(('AT+CMGS="'+number+'"\r').encode())
	time.sleep(1)
	ser.write((msg+chr(26)+'"\r').encode())
	tnow =	datetime.datetime.now()
	current_time =	tnow.strftime("%H:%M:%S")
	print("["+colored(current_time,"blue")+"] "+colored("Send SMS To : ","cyan",attrs=['bold'])+number)
	print("["+colored(current_time,"blue")+"] "+colored("SMS Message : ","cyan",attrs=['bold'])+msg)
	return True
def	advancedcall(mobile):
	if cc!="+30":
		mobile=cc+mobile
	g=False
	ser.write('ATZ\r'.encode())
	ser.write(('ATD '+mobile+';\r').encode())
	tnow =	datetime.datetime.now()
	current_time =	tnow.strftime("%H:%M:%S")
	print("["+colored(current_time,"blue")+"] "+colored("Advanced Call To : ","green",attrs=['bold'])+mobile)
	time.sleep(3)
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
					#print("Status : "+g)
					sbool=False
				if g=="0" or "+CLCC: 1,0,0" in ddata:
					break
			if "1,0,0" in data.decode():
				g="0"
				break
			counter+=1
			if counter==40:
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
		if onlydetect==False:
			snapsms(mobile)
		if checkstarts(mobile)==True:
			if mobile not in open(outfile).read():
				with open(outfile, "a") as myfile:
					myfile.write(mobile+"\r\n")
def	missedcall(mobile):
	if cc!="+30":
		mobile=cc+mobile
	ser.write('ATZ\r'.encode())
	ser.write(('ATD '+mobile+';\r').encode())
	tnow =	datetime.datetime.now()
	current_time = tnow.strftime("%H:%M:%S")
	print("["+colored(current_time,"blue")+"] "+colored("Missed Call To : ","green",attrs=['bold'])+mobile)
	time.sleep(7)
	ser.write('ATZ\r'.encode())
	ser.write('AT+CHUP\r'.encode())
	time.sleep(0.5)
def listlen():
	if os.path.exists(outfile):
		with open(outfile) as f:
			lines = f.readlines()
			print(colored(str(len(lines))+" active mobile numbers in "+outfile,"blue",attrs=['bold']))
delcounter=1
delbool=True
detnumbers=[]
now=datetime.datetime.now()
now	= now +	datetime.timedelta(0,10)
if missed==False and advanced==False and enablesms==False:
	print(colored("Only Detecting Incoming Calls And SMS","red",attrs=['bold']))
	print(" sudo python3 telebloatballs.py -h ")
else:
	print(colored("Detecting Incoming Calls And SMS","blue",attrs=['bold']))
if advanced==True:
	print(colored("Detecting Outgoing Advanced Calls","blue",attrs=['bold']))
if missed==True:
	print(colored("Detecting Outgoing Missed Calls","blue",attrs=['bold']))
if enablesms==True:
	print(colored("Sending SMS","blue",attrs=['bold']))
else:
	print(colored("Sending SMS On Detections","blue",attrs=['bold']))
listlen()
while True:
	if	now	< datetime.datetime.now():
		delcounter+=1
		delbool=True
		if advanced==True:
			advancedcall(randomnum())
		if missed==True:
			for x in range(missedcounter):
				missedcall(randomnum())
		if enablesms==True:
			smscount=0
			with open(smslist, 'r', encoding='utf-8', errors='ignore') as f:
				for line in f:
					num = normalize_number(line)
					smsbool =snapsms(num,sendfile)
					if smsbool==True:
						smscount+=1
						print(colored("SMS Count : ","green",attrs=['bold'])+str(smscount))
						if num not in open(sendfile).read():
							with open(sendfile, "a") as myfile:
								myfile.write(num+"\r\n")
						time.sleep(5)
						now=datetime.datetime.now()
						now=now+datetime.timedelta(0,3)
			sys.exit()
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
			'''if data.decode()!="":
				print (data)'''
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
					time.sleep(2)
					if onlydetect==False:
						snapsms(mnum)
					mnumbers.append(mnum)
					detnumbers.append(mnum)
				mdata=mdata.replace(rep,"")
			if len(mnumbers)>0:
				for x in mnumbers:
					if checkstarts(x)==True:
						if	x not in open(outfile).read():
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
					time.sleep(2)
					if onlydetect==False:
						snapsms(mnum)
					mnumbers.append(mnum)
					detnumbers.append(mnum)
				mdata=mdata.replace(rep,"")
			if len(mnumbers)>0:
				for x in mnumbers:
					if checkstarts(x)==True:
						if	x not in open(outfile).read():
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
					if phonenumber not in open(outfile).read():
						print("["+colored(current_time,"blue")+"] "+colored("Detected Number : ", 'red',attrs=['bold'])+phonenumber)
						if onlydetect==False:
							snapsms(phonenumber)
						with open(outfile, "a") as myfile:
							myfile.write(phonenumber+"\r\n")
				#Close the Phone
				ser.write('ATZ\r'.encode())
				time.sleep(1)
				ser.write('AT+CHUP\r'.encode())
				time.sleep(1)
		except:
			pass
