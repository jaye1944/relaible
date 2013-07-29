import socket
import pickle
import time
import math
import resive_data

UDP_IP = "127.0.0.1"
UDP_PORT = 5000
SERVER_PORT = 5005
#ACKS
ACKPOSITIVE = "P"
ACKNEGATIVE = "N"

def FirstACK():
    while True:
        sock.sendto(ACKPOSITIVE.encode('utf-8'), (UDP_IP, SERVER_PORT))
        data, addr = sock2.recvfrom(100)
        return data
        break

def window_Ack(infor):
    while True:
        sock.sendto(infor.encode('utf-8'),(UDP_IP, SERVER_PORT))
        break

def collector(temp,original):
    for i in range(0,len(temp)):
        if temp[i] != b'':
            original.append(temp[i])
    temp = []


def list_ack(lst):
    if len(lst)== 0:
        window_Ack(ACKPOSITIVE)
    else:
        rr = ""
        for i in range(0,len(lst)):
            rr += str(lst[i])
            rr += " "
        window_Ack(rr)

def list_maker(ori_file,no_c,w_c):
    if no_c - len(ori_file) >= w_c:
        temp_store = [None]*w_c
    else:
        temp_store = [None]*(no_c%w_c)
    return temp_store

def re_resiver(t_store):
    while True:
        data, addr = sock2.recvfrom(2048)
        get_packet = pickle.loads(data)
        dat = resive_data.datapart(get_packet)
        if dat == b'':
           window_Ack(ACKNEGATIVE)
        elif resive_data.error_two(get_packet):
            for i in range(0,len(t_store)):
                if t_store[i]== None :
                    t_store[i] = dat
                    break
            window_Ack(ACKPOSITIVE)
        else:
            window_Ack(ACKNEGATIVE)
        if not None in t_store:
            break

def stopper(start,ori_file,CH,actual_errors,error_free):
    if(len(ori_file)==CH):
        end = time.time()# now file transfer is over
        resive_data.print_All(str(end - start),actual_errors,error_free)#print results
        resive_data.writer(ori_file)#create a file
        return True
    return False

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
            temp_store[resive_data.pac_number(get_packet)] = resive_data.datapart(get_packet)
        else:
            actual_errors +=1
            error_pac_num_list.append(resive_data.pac_number(get_packet))
        if(pac_in_window == len(temp_store)):#check window size
            window_count +=1
            list_ack(error_pac_num_list)
            if not None in temp_store:#all packets are ok
                collector(temp_store,original_file) #add data
                if(stopper(start,original_file,NUM_OF_CHUNKS,actual_errors,error_free)):#comaire error free packets with how many actual packets
                    break
                temp_store = list_maker(original_file,NUM_OF_CHUNKS,WINDOW_SIZE)
                 # + Ack
            else:#some pacs lost
                re_resiver(temp_store)
                collector(temp_store,original_file)
                if(stopper(start,original_file,NUM_OF_CHUNKS,actual_errors,error_free)):#comaire error free packets with how many actual packets
                    break
                temp_store = list_maker(original_file,NUM_OF_CHUNKS,WINDOW_SIZE)
            error_pac_num_list = []
            pac_in_window = 0


print("UDP target IP: " + UDP_IP)
print("UDP target port: " + str(UDP_PORT))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock2.bind((UDP_IP, UDP_PORT))

start()