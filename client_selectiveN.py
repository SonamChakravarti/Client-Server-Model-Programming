####################CSC 573 PROJECT 2- SIMPLE FILE TRANSFER PROTOCOL USING RELIABLE UDP####################

#Submitted BY: Sonam Chakravarti and Samarth Asthana
#Date: April 21st,2013
#File: client.py

###########################################################################################################
from collections import deque
import sys
import thread
import socket
import sys
from collections import deque
import time
import copy
from datetime import datetime
#checksum function
def carry_around_add(a, b):
    			c = a + b
   		 	return (c & 0xffff) + (c >> 16)

def checksum(msg):
    			s = 0
    			for i in range(0, len(msg), 2):
        			w = ord(msg[i]) + (ord(msg[i+1]) << 8)
        			s = carry_around_add(s, w)
    			return ~s & 0xffff

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server-host-name server-port# file-name N MSS
USAGE = 'Usage: client server-host-name server-port# filename Window Size MSS'
if len (sys.argv) != 6:
	print USAGE
	sys.exit (1)
host=sys.argv[1]
port=int(sys.argv[2])
flag=0
seq=0
acked=''
inseq=''
insequence=''
d=list()
e=deque()
length=0
MSS=int(sys.argv[5])
N=0
windowSize=int(sys.argv[4])
temp=''
msg=''
check=''
che=''
age=0
test=''
count=0
get=''
current=0
server_address = (host, port)
#####################################send function#################################
def snd(threadname):
 while 1:		
    global d,windowSize,flag,MSS,temp,msg,check,inseq,seq,insequence,che,server_address,sock,f,length,get,current
    while(len(d)<windowSize and flag!=9999999):
		while(flag<MSS):
			c = f.read(1)
			if not c:
				flag=9999999
 				break
			temp=temp+c
			flag=flag+1
		inseq=str(seq)
		insequence=inseq.zfill(10)
		check=checksum(insequence)
		che=str(check).zfill(10)
		msg=insequence+temp+che
		d.append(msg)
		sent = sock.sendto(msg, server_address)
		if(flag==9999999):
			break
		seq=seq+len(temp)	
		temp=''
		inseq=''
		insequence=''
		msg=''
		
		flag=0    
    if(flag==9999999 and len(d)==0):
	break				
###################################################################################
#####################################receive function##############################
def rcv(threadname):
     while 1:	
		global d,test,sock,count,e,current,MSS,flag
		data, server = sock.recvfrom(4096)
		nack='NACK'
		if(data.startswith(nack)):
			data=data[4:]
			print>>sys.stderr,"Timeout, sequence number = %d"%(int(data))
			t=0
			clash=''
			if(len(d)!=0):
			  while(t<len(d)):
				clash=d[t]
				t=t+1
				if(clash.find(data)):
					sent = sock.sendto(clash, server_address)
					clash=''
					break
			
		elif(data.startswith('ERROR')):
			data=data[5:]
			#print>>sys.stderr,"Timeout, sequence number = %d"%(int(data))
			t=0
			clash=''
			if(len(d)!=0):
			  while(t<len(d)):
				clash=d[t]
				t=t+1
				if(clash.find(data)):
					sent = sock.sendto(clash, server_address)
					clash=''
					break
		else:
			t=0
			if(len(d)!=0):
				if(data in d):
				             d.remove(data)
				
                if(flag==9999999 and len(d)==0):
			break
###################################################################
#####################Start Threads for send and recieve############################
f=open(sys.argv[3],'r')
tstart=datetime.now()
try:
	   thread.start_new_thread( snd, ("Thread-1",  ) )
	   thread.start_new_thread( rcv, ("Thread-2",  ) )
except:
   	   print "Error: unable to start thread"
time.sleep(300)
tend=datetime.now()
#print tend-tstart
sys.exit(1)
	
