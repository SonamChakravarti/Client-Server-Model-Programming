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
def carry_around_add(a, b):
    			c = a + b
    			return (c & 0xffff) + (c >> 16)

def checksum(msg):
    		s = 0
    		for i in range(0, len(msg), 2):
        		w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        		s = carry_around_add(s, w)
    		return ~s & 0xffff
USAGE = 'Usage: server port# file-name probability'
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
nack=''
nom=0
target='END OF FILE'
seqr=''
filed=list()
rand=float(0)
probability=float(sys.argv[3])
host = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | grep -iv \"inet6\" | " +
                         "awk {'print $2'} | sed -ne 's/addr\:/ /p'")
print >>sys.stderr,host
server_address = ('', int(sys.argv[1]))
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
while True:
  	rand=float(random.uniform(0,1))	
   	data, address = sock.recvfrom(4096)
	if(add!=address):
		add=address
		ack=0	
  	if (rand>probability):
			test=data[0:10]
			check=checksum(test)
			if(data[len(data)-10:len(data)]==str(check).zfill(10)):
				ack=len(test)
				mes=data
				wish=0
				sent = sock.sendto(mes, address)
				if(not(data in filed)):
					filed.append(data)
				filed.sort()
				fo = open(sys.argv[2], "w")
				t=0
				n=0
				yay=''
				while(t<len(filed)):	
					yay=filed[t]
					n=len(filed[t])
					fo.writelines(yay[10:n-10])
					t=t+1
				fo.close()
			else:	
				wish=1
	if(rand<=probability and wish==0):
		nom=int(data[0:10])
		print>>sys.stderr,"Packet loss, sequence number = %d"%nom
		nack='NACK'+data[0:10]
	        sent = sock.sendto(nack, address)
		
	if(wish==1):
		err='ERROR'+data[0:10]
		sent = sock.sendto(err, address)
    	
