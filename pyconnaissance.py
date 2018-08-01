from netifaces import AF_INET
import netifaces as nf
import datetime
import sys
import os
import subprocess

if len(sys.argv)!=3:

	print("Usage: python3 pyconnaissance.py <interface> <log file>")

	exit()

def get_local_addr():

	local_addr=nf.ifaddresses(sys.argv[1])[AF_INET][0]['addr']

	return local_addr

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

def netmap(range_ip):

	os.system("nmap -T4 -O -sV -oX - "+range_ip+" > "+sys.argv[2]+".xml")

def xml_to_html():

	os.system("xsltproc "+sys.argv[2]+".xml > "+sys.argv[2]+".html")
	
	os.system("rm "+sys.argv[2]+".xml")

start_time = datetime.datetime.now()

f=open(sys.argv[2], "w+")

f.write("Started at "+str(start_time)+"\n")

f.write("Host Address: "+get_local_addr()+"\n")

ip_range=get_ip_range()

default_gateway=get_default_gateway()

f.close()

netmap(ip_range)

xml_to_html()





	
	
