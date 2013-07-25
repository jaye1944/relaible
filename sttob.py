
from threading import Thread
from time import sleep

def threaded_function(arg):
    #for i in range(arg):
    while True:
        print("running")
        sleep(1)

def stop_function(arg):
    while True:
        id = input("Do you want to stop : ")
        if (id == "y"):
            arg._stop()
            break
        print("while loop")


#if __name__ == "__main__":
#thread1 = Thread(target = threaded_function, args = (100, ))
#thread = Thread(target = stop_function, args = (thread1, ))
#thread1.start()

#thread.start()
pre_list = [None]*5
pre_list[4] = 6
pre_list[2] = 6
pre_list[0] = 6
pre_list[1] = 6
pre_list[3] = 6
print(pre_list)
if None in pre_list:
    print("Not Full")