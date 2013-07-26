import socket
import pickle
import time
import math
import resive_data

UDP_IP = "127.0.0.1"
UDP_PORT = 5000
SERVER_PORT = 5005
#ACKS
ACKPOSITIVE = "1"

def FirstACK():
    while True:
        sock.sendto(ACKPOSITIVE.encode('utf-8'), (UDP_IP, SERVER_PORT))
        data, addr = sock2.recvfrom(100)
        return data
        break

def window_Ack(infor):
    while True:
        sock.sendto(infor.encode('utf-8'),(UDP_IP, SERVER_PORT))
        #data, addr = sock2.recvfrom(100)
        #return data
        break

def list_ack(lst):
    while True:
        sock.sendto(pickle.dumps(lst),(UDP_IP, SERVER_PORT))
        break

#ready to get data
#print(FirstACK())
def start():
    alldata = FirstACK().decode('utf-8').split(" ")
    print(".....Resive from server....")
    print("File name is " + alldata[0])
    print("File number of chunks are " + alldata[1])
    print("File chunk size is " + alldata[2] + " bytes")
    print("File Window size is " + alldata[3])
    WINDOW_SIZE = int(alldata[3])
    NUM_OF_CHUNKS = int(alldata[1])
    #make environment
    resive_data.ffname = alldata[0] +"1"
    resive_data.sq = math.sqrt(int(alldata[1])) #pass sqrt of chunk to uniform distributin
    pac_in_window = 0 #number in window pac
    window_count = 0 #which window

    global original_file
    original_file =[] #data array
    actual_errors = 0 #how many error packets resived
    error_free = 0 # how many error free packets resived

    #send ack for ready
    if NUM_OF_CHUNKS >= WINDOW_SIZE:
        temp_store = [None]*WINDOW_SIZE
    else:
        temp_store = [None]*NUM_OF_CHUNKS
    error_pac_num_list = []
    sock.sendto(ACKPOSITIVE.encode('utf-8'), (UDP_IP, SERVER_PORT))
    start = time.time()
    while True:
        data, addr = sock2.recvfrom(2048) # buffer size is 2048 bytes
        get_packet = pickle.loads(data) #load data from packet
        pac_in_window +=1
        if resive_data.error(get_packet,pac_in_window-1):#check the errors
            error_free += 1
            temp_store[resive_data.window_number(get_packet)] = resive_data.datapart(get_packet)
            #print(temp_store)
            if not None in temp_store:
                for i in range(0,len(temp_store)):
                    original_file.append(temp_store[i])
                if NUM_OF_CHUNKS - len(original_file) >= WINDOW_SIZE:
                    temp_store = [None]*WINDOW_SIZE
                else:
                    temp_store = [None]*(NUM_OF_CHUNKS%WINDOW_SIZE)
            if(len(original_file) == NUM_OF_CHUNKS):#comaire error free packets with how many actual packets
                end = time.time()# now file transfer is over
                resive_data.print_All(str(end - start),actual_errors,error_free)#print results
                resive_data.writer(original_file)#create a file
                break
        else:
            actual_errors +=1
            error_pac_num_list.append(resive_data.window_number(get_packet))
        if(pac_in_window == WINDOW_SIZE):#check window size
            window_count +=1
            list_ack(error_pac_num_list)
            if len(error_pac_num_list) == 0:
                print("good")
                 # + Ack
            else:
                print("bad")
                #list_ack(error_pac_num_list)
            error_pac_num_list = []
            pac_in_window = 0


print("UDP target IP: " + UDP_IP)
print("UDP target port: " + str(UDP_PORT))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock2.bind((UDP_IP, UDP_PORT))

start()