import random
global ffname
global sq

global error_ratio
error_ratio = 0.5

def error_or_not():
    ra = random.randrange(0,int(sq))
    if(ra < sq*error_ratio):
        return True
    return False

def error(dict,seqnumber):    #simple error checking
    for i,j in dict.items():
        for p,q in j.items():
            if( p == q.__hash__() and (seqnumber == i)):#check error using hash value and fram
               # simulation error using uniform distributuion
                if(error_or_not()):
                   return False
                return True
    return False

def error_two(dict):
    for i,j in dict.items():
        for p,q in j.items():
            if p == q.__hash__():#check error using hash value
               # simulation error using uniform distributuion
                if(error_or_not()):
                   return False
                return True
    return False

def writer(or_file):
    f = open(ffname, 'wb')
    for i in or_file:
        f.write(i)
    f.close()
   # os.remove(f)

def datapart(dict):
    for i,j in dict.items():
        for p,q in j.items():
            return q

def pac_number(dict):
    for i,j in dict.items():
        return i

def print_All(time,errors,noterrors):
    print("\n------- Results-------")
    print("Time " + time)
    print("File resived compleatly")
    print("Error packets resived " + str(errors))
    print("Error free resived "+ str(noterrors))
    print("Total packets "+ str(errors+noterrors))
    print("Calcualated Error ratio "+ str(errors/(errors+noterrors)))
    print("Original error "+ str(error_ratio))

