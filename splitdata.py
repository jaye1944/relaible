
file_size = 100 #coose packet size as 100 bytes
def spliter(inputFile,chunksize):

#read
    f = open(inputFile, 'rb')
    data = f.read() # read the entire content of the file
    f.close()

    bytes = len(data)
    noOfChunks= bytes/chunksize
    #print ("now berore" + str(noOfChunks))
    if(bytes%chunksize):
        noOfChunks+=1
    chunkNames = []
    for i in range(0, bytes, chunksize):
       # print(i)
        fn1 = "chunk" + str(i+100)
        chunkNames.append(fn1)
        f = open(fn1, 'wb')
        goto = []
       # data[100] = int(48)
        wind = 5
        goto= data[i:i+chunksize]
        print(sum(goto))
        packet ={str(wind):{sum(goto):goto}}
       # mydic[0] = goto
        #goto.append("22")
        f.write(goto) #write 100 by 100byte data
    f.close()
    print(chunkNames)



spliter("TT",file_size)
