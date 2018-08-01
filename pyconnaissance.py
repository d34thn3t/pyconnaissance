from netifaces import AF_INET
import netifaces as nf
import datetime
import sys
import os
import subprocess

#make sure all arguments are provided, if not then exit with this message

if len(sys.argv)!=3:

	print("Usage: python3 pyconnaissance.py <interface> <log file>")

	exit()
	
#get host address on current interface

def get_local_addr():

	local_addr=nf.ifaddresses(sys.argv[1])[AF_INET][0]['addr']

	return local_addr

#get range of ip addresses to be used by nmap

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

	os.system("nmap -sU -T4 -p1-65535 -O -sV -oX - "+range_ip+" > "+sys.argv[2]+".xml")
	
#convert nmap's xml output to html

def xml_to_html():

	os.system("xsltproc "+sys.argv[2]+".xml > "+sys.argv[2]+".html")
	
	os.system("rm "+sys.argv[2]+".xml")
	
#main code

#get start time

start_time = datetime.datetime.now()

#create log file 

f=open(sys.argv[2], "w+")

#write time into log file

f.write("Started at "+str(start_time)+"\n")

#write host address into log file

f.write("Host Address: "+get_local_addr()+"\n")

#set value to the ip range for nmap

ip_range=get_ip_range()

#set value to router ip

default_gateway=get_default_gateway()

#close main log

f.close()

#run nmap

netmap(ip_range)

#conver xml output of nmap to html

xml_to_html()





	
	
