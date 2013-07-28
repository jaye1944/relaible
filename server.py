import socket
import datahandle
import pickle
#from threading import Thread

#server data
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
CLIENT_PORT = 5000
#file info
CHUNK_SIZE = 100
WINDOW_SIZE = 5
SEND_FILE = "myfile.txt" #file name which going to send

#ACKS
ACKPOSITIVE = "1"


def sendACK(first_data):
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 1024 bytes
        if (data.decode('utf-8') == ACKPOSITIVE):
            sock2.sendto(first_data.encode('utf-8'), (UDP_IP, CLIENT_PORT))
            break

def WAIT():
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 100bytes
        if (data.decode('utf-8') == ACKPOSITIVE):
            break

def Window_Ack():
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 100 bytes
        return pickle.loads(data)
        break
#------------------------------------------------------
def ack_listener():
    while True:
        data, addr = sock.recvfrom(100)
        print("from method")
        print(data.decode('utf-8'))
        return data.decode('utf-8')
        break

#--------------------------------------------------------------
def resender(t_store,error_list):
    for i in range(0,len(error_list)):
        #print(t_store[error_list[i]])
        print(error_list)
        de_data = "0"
        while de_data != ACKPOSITIVE:
            #print(de_data)
            sock2.sendto(t_store[error_list[i]],(UDP_IP, CLIENT_PORT))
            #print("data send")
            de_data = ack_listener()
            print(de_data)




def transfer():
    windowframe = 0 #window frame number
    i =0 #chunk increasere
    NO_OF_CHUNKS = datahandle.no_of_chun(SEND_FILE, CHUNK_SIZE)
    temp_store = []
    while True:
        if(windowframe == WINDOW_SIZE ):
            windowframe = 0
            k = Window_Ack()
            if(len(k)!= 0):
                print("Negative ack resive")
                #i = i - ((int(k) + WINDOW_SIZE) * CHUNK_SIZE )#re arrange the window in data buffer
                resender(temp_store,k)
                temp_store = []
            else:
                print("Positive ack resive")
                temp_store = []
                #k = ACKPOSITIVE
        data_part = data_to_send[i:i+CHUNK_SIZE]
        i += CHUNK_SIZE
        packet={windowframe:{data_part.__hash__():data_part}} #add data and metadata to dictionary hash value of data
        send_packet = pickle.dumps(packet) #make one packet
        temp_store.append(send_packet)
        try:
            sock2.sendto(send_packet,(UDP_IP, CLIENT_PORT)) #send data
        except Exception:
            print("Connection error")
            break
        #print("frame " + str(windowframe) + " send")
        windowframe +=1

print("Server IP " + UDP_IP +" Srever port "+ str(UDP_PORT))
print("Window size is "+ str(WINDOW_SIZE))
print("Chunk size is "+ str(CHUNK_SIZE))
print("Ready to connect......")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# resiver
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data_to_send = datahandle.get_data(SEND_FILE)#get data array
firstdata = datahandle.get_file_info(SEND_FILE, CHUNK_SIZE) + " " + str(WINDOW_SIZE)#first information

sendACK(firstdata)#check the connection of the server and send send data about the file
print(datahandle.no_of_chun(SEND_FILE, CHUNK_SIZE))
#file_size = len(data_to_send)#get the size of the file from bytes
WAIT() #wait till the resiver ready to get data

transfer()


