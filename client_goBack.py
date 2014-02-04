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

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
USAGE = 'Usage: client host port# filename Window Size MSS'
if len (sys.argv) != 6:
	print USAGE
	sys.exit (1)
####################declarations#####################################
host=sys.argv[1]
port=int(sys.argv[2])
flag=0
seq=0
localseq=0
loc=''
lon=0
nacked=''
inseq=''
insequence=''
d=list()
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
send_all=0
stuff=''
count=0
get=''
current=0
#####################################################################
server_address = (host, port)
#####################################send function#################################
def snd(threadname):
 while 1:		
    global d,windowSize,flag,MSS,temp,msg,check,inseq,seq,insequence,che,server_address,send_all,sock,f,length,get,current
    while(len(d)<windowSize and send_all!=1 and flag!=9999999):
		while(flag<MSS):
			c = f.read(1)
			if not c:
				flag=9999999
 				break
			temp=temp+c
			flag=flag+1
		if(MSS==1):
			flag=0
		inseq=str(seq)
		insequence=inseq.zfill(10)
		check=checkit(insequence)
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
    #print d
    if(flag==9999999 and len(d)==0):
	break			
###################################################################################
#####################################receive function##############################
def rcv(threadname):
     while 1:
               # print 'run2'	
		global d,test,send_all,sock,count,e,current,MSS,flag,stuff
		data, server = sock.recvfrom(4096)	
		if(len(d)!=0):
			test=str(d[0])
			age=int(test[0:10])+len(d[0])-20
			if(age==int(data[0:10])):	
					current=1
		      			d.pop(0)
					current=0
			
				   
                if(flag==9999999 and len(d)==0):
                 	break
#############################################################################
#######################resend function#######################################
def resend(threadname):
	 while 1:
		global stuff,send_all,length,d,current,sock,count,loc,localseq
		localdata=''
		localdata=stuff
		time.sleep(.5)
		if(localdata==stuff or localdata==''):
			send_all=1
			if(stuff!=''):
				loc=stuff[0:10]
			else:
				loc='0'
			localseq=int(loc)
		        if(send_all==1 and len(d)!=0 and current==0):
			    length=len(d)
			    while(length!=0 and current==0 and len(d)!=0):
			   	 nack=d[len(d)-length]	
			    	 print>>sys.stderr,"Timeout, sequence number = %d"%(int(nack[0:10]))					
				 sent = sock.sendto(d[len(d)-length], server_address)
				 length=length-1
   	                    send_all=0
			    	
    		        elif(send_all==1 and len(d)==0):
					  send_all=0
		if(flag==9999999 and len(d)==0):
                 	break
###################################################################################
#####################Start Threads for send and recieve############################
f=open(sys.argv[3])
tstart = datetime.now()
try:
	   thread.start_new_thread( snd, ("Thread-1",  ) )
	   #print ' here'	
	   thread.start_new_thread( rcv, ("Thread-2",  ) )
	   thread.start_new_thread( resend, ("Thread-3",  ) )
except:
   	   print "Error: unable to start thread"
time.sleep(300)
tend = datetime.now()
#print (tend-tstart)
sys.exit(1)

	
