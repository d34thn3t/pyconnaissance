# pyconnaissance
An automatic network reconaissance script.
Developed for an automated reconaissance system I wanted to use on a Raspberry Pi running Kali Linux.
OS: Any Linux Flavor(Recommended: Kali 2018.3)
Required programs: nmap, python3
Required Python modules: netifaces

Usage: python3 pyconnaissance.py <interface> <log file name>
  
It will save basic information such as host IP, router IP and IP address range in a log file with no extension.
Information gathered by nmap will be stored in an HTML file.
It will sniff the network and store various types of information in different files.

More Features will be added soon.

