import socket
import datahandle
import pickle
from threading import Thread

#server data
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
#file info
CHUNK_SIZE = 100
WINDOW_SIZE = 5
SEND_FILE = "H.jpg" #file name which going to send

#ACKS
ACKPOSITIVE = "1"

print("Server IP " + UDP_IP +" Srever port "+ str(UDP_PORT))
print("Window size is "+ str(WINDOW_SIZE))
print("Chunk size is "+ str(CHUNK_SIZE))
print("Ready to connect......")
def sendACK(first_data):
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 1024 bytes
        if (data.decode('utf-8') == ACKPOSITIVE):
            sock2.sendto(first_data.encode('utf-8'), (UDP_IP, 5000))
            break

def WAIT():
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 1024 bytes
        if (data.decode('utf-8') == ACKPOSITIVE):
            break

def Window_Ack():
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 1024 bytes
        return data.decode('utf-8')
        break
#------------------------------------------------------
def ack_listener(arg):
    while True:
        data, addr = sock.recvfrom(100)
        print(data.decode('utf-8'))
        break

#--------------------------------------------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# resiver
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data_to_send = datahandle.get_data(SEND_FILE)#get data array
firstdata = datahandle.get_file_info(SEND_FILE, CHUNK_SIZE) + " " + str(WINDOW_SIZE)#first information

sendACK(firstdata)#check the connection of the server and send send data about the file

file_size = len(data_to_send)#get the size of the file from bytes
WAIT() #wait till the resiver ready to get data

def transfer(arg):
    packet = {} #data packet
    windowframe = 0 #window frame number
    i =0 #chunk increasere
    while True:
        if(windowframe == WINDOW_SIZE ):
            windowframe = 0
            k = Window_Ack()
            if(k!= ACKPOSITIVE):
                print("Negative ack resive")
                i = i - ((int(k) + WINDOW_SIZE) * CHUNK_SIZE )#re arrange the window in data buffer
            else:
                print("positive ack resive")
                k = ACKPOSITIVE
        data_part = data_to_send[i:i+CHUNK_SIZE]
        i += CHUNK_SIZE
        packet={windowframe:{data_part.__hash__():data_part}} #add data and metadata to dictionary
        send_packet = pickle.dumps(packet) #make one packet
        sock2.sendto(send_packet,(UDP_IP, 5000)) #send data
        print("frame " + str(windowframe) + " send")
        windowframe +=1

#transfer()

#--------------------------------------------------------------------
#create listen thread....
if __name__ == "__main__":
    trns = Thread(target = transfer, args = ("pop", ))
    trns.start()
    ##listener = Thread(target = ack_listener, args = ("pop", ))
    #listener.start()

#------------------------------------------------------------------

#listener.start()

