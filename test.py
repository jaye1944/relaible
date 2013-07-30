lltt = [1,22,3,4,5,6]
strh = str(lltt)
strh = strh.split(", ")
#logs = strh.split(", ")
tt = 0

def incre():
    global tt
    tt += 1

for i in range(0,10):
    incre()

def pr():
    print(tt)

pr()

