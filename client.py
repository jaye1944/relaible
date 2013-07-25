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

print("UDP target IP: " + UDP_IP)
print("UDP target port: " + str(UDP_PORT))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock2.bind((UDP_IP, UDP_PORT))

#ready to get data
#print(FirstACK())
alldata = FirstACK().decode('utf-8').split(" ")
print(".....Resive from server....")
print("File name is " + alldata[0])
print("File number of chunks are " + alldata[1])
print("File chunk size is " + alldata[2] + " bytes")
print("File Window size is " + alldata[3])
#make environment
resive_data.ffname = alldata[0] +"1"
resive_data.sq = math.sqrt(int(alldata[1])) #pass sqrt of chunk to uniform distributin
count_packets = 0 #which packets
pac_in_window = 0 #number in window pac
window_count = 0 #which window
global lock      #use to lock the errorless list from error list
lock = True

global original_file
original_file =[] #data array
actual_errors = 0 #how many error packets resived
error_free = 0 # how many error free packets resived

#send ack for ready
sock.sendto(ACKPOSITIVE.encode('utf-8'), (UDP_IP, SERVER_PORT))
start = time.time()

while True:
    data, addr = sock2.recvfrom(2048) # buffer size is 2048 bytes
    get_packet = pickle.loads(data) #load data from packet
    pac_in_window +=1
    if resive_data.error(get_packet,pac_in_window-1):#check the errors
        error_free += 1
        if(lock):# can add data to array
            count_packets +=1
            original_file.append(resive_data.datapart(get_packet))
            #print("Length " +str(len(original_file)))
            if(count_packets == int(alldata[1])):#comaire error free packets with how many actual packets
                end = time.time()# now file transfer is over
                resive_data.print_All(str(end - start),actual_errors,error_free)#print results
                resive_data.writer(original_file)#create a file
                break
    else:
        actual_errors +=1
        if(lock):
            error_pac_no = resive_data.window_number(get_packet)
        lock = False #ignore all data after the error
    if(pac_in_window == int(alldata[3])):#check window size
        window_count +=1
        if(lock):
            window_Ack(ACKPOSITIVE) # + Ack
        else:
            window_Ack(str(-(error_pac_no)))
            error_list = [] #free the list
            lock = True
        pac_in_window = 0
