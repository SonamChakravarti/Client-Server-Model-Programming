####################CSC 573 PROJECT 2- SIMPLE FILE TRANSFER PROTOCOL USING RELIABLE UDP####################

#Submitted BY: Sonam Chakravarti and Samarth Asthana
#Date: April 21st,2013
#File: server.py

###########################################################################################################

import socket
import sys
import commands
import random
import time

#print ips
#Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#define function to calcuate checksum and carry 
def carry(in1, in2):
   		 in3 = in1 + in2
    		 return (in3 & 0xffff) + (in3 >> 16)

def checkit(msg):
    		a = 0
    		for i in range(0, len(msg), 2):
        		b = ord(msg[i]) + (ord(msg[i+1]) << 8)
        		a = carry(a, b)
    		return ~a & 0xffff
USAGE = 'Usage: server port# filename probability'
if len (sys.argv) != 4:
		print USAGE
		sys.exit (1)
check=0
ack=0
err=''
test=''
temp=''
wish=0
last=0
add=''
rand=float(0)
probability=float(sys.argv[3])
#display host ip addresses which are available
host = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | grep -iv \"inet6\" | " +
                         "awk {'print $2'} | sed -ne 's/addr\:/ /p'")
print >>sys.stderr,host
server_address = ('', int(sys.argv[1]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
while True:
	#generate random number
  	rand=float(random.uniform(0,1))
	#recieve data from sender	
   	data, address = sock.recvfrom(4096)
	#if new client reset the ack to 0
	if(add!=address):
		add=address
		ack=0	
	#random probablity should be greater than input to accept a packet
  	if (rand>probability):
		temp=str(ack).zfill(10)
		if(int(data[0:10])==int(temp)): #check if expected pacted has arrived
			test=data[0:10]
			check=checkit(test)
			if(data[len(data)-10:len(data)]==str(check).zfill(10)):#check if correct data using checksum
				ack=ack+(len(data)-20)
				last=ack
				mes=str(ack).zfill(10)+'AAAA'+'0000'
				wish=0
       				sent = sock.sendto(mes, address)
				f=open(sys.argv[2],'a') #append data into previous file
		 		f.writelines(data[10:len(data)-10])
				f.close();#close file
			else:	
				wish=1 # checksum failed
		else:
				wish=1 # unexpected packet
	if(rand<=probability and wish==0): #packet loss due to probability
		print>>sys.stderr,"Packet loss, sequence number = %d"%ack
		
    	
