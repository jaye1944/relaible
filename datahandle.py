

def get_data(inputfile):
    f = open(inputfile, 'rb')
    data = f.read() # read the entire content of the file
    f.close()
    return data

def get_file_info(inputfile,splitsize):
    bytes = len(get_data(inputfile))
    noOfChunks= bytes/splitsize
    if(bytes%noOfChunks):
        noOfChunks+=1
    infomation = str(inputfile)+" "+str(int(noOfChunks))+" "+ str(splitsize)
    return infomation

def no_of_chun(inputfile,splitsize):
    bytes = len(get_data(inputfile))
    noOfChunks= bytes/splitsize
    if(bytes%noOfChunks):
        noOfChunks+=1
    return int(noOfChunks)
