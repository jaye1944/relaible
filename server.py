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
ACKPOSITIVE = "P"


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
    #data = []
    #while data != None:
    data, addr = sock.recvfrom(500)  # buffer size is 100 bytes
        #rrr =
    return pickle.loads(data)

#------------------------------------------------------
def ack_listener():
    data, addr = sock.recvfrom(100)
    return data.decode('utf-8')


#--------------------------------------------------------------
def resender(t_store,error_list):
    for i in range(0,len(error_list)):
        #print(t_store[error_list[i]])
        print(error_list)
        de_data = "0"
        while de_data != ACKPOSITIVE:
            sock2.sendto(t_store[error_list[i]],(UDP_IP, CLIENT_PORT))
            de_data = ack_listener()
            print(de_data)

def lst_maker(stri):
    str_li = stri.split(" ")
    int_li = []
    for i in range(0,len(str_li)-1):
        int_li.append(int(str_li[i]))
    return int_li


def transfer():
    windowframe = 0 #window frame number
    i =0 #chunk increasere
    NO_OF_CHUNKS = datahandle.no_of_chun(SEND_FILE, CHUNK_SIZE)
    temp_store = []
    while True:
        if(windowframe == WINDOW_SIZE ):
            windowframe = 0
            k = lst_maker(ack_listener())
            print(k)
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


