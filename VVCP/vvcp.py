#Dependencies (to pip install):
#moviepy
#beetroot

#function things

import datetime
import os
import sys

curdir = os.path.dirname(os.path.abspath(sys.argv[0]))

def time():
    yeet = datetime.datetime.now().today()

    yeet = [
        str(yeet.year),
        str(yeet.month),
        str(yeet.day),
        str(yeet.hour),
        str(yeet.minute),
        str(yeet.second)
    ]
    
    return yeet[1] + "/" + yeet[2] + "/" + yeet[0] + ":" + yeet[3] + ":" + yeet[4] + ":" + yeet[5]

with open(curdir + "/latest.log", "w") as f:
    pass

def log(mode, text):
    #logger ig
    with open(curdir + "/latest.log", "r") as f:
        logd = f.read()
    
    with open(curdir + "/latest.log", "w") as f:
        curt = time()
        if mode == 0:
            logd = "\n".join(
                [
                    logd,
                    f"[{curt}] [DEBUG]: {text}"
                ]
            )
            f.write(logd)
            return 0
            
        elif mode == 1:
            logd = "\n".join(
                [
                    logd,
                    f"[{curt}] [WARNING]: {text}"
                ]
            )
            f.write(logd)
            return 0
            
        elif mode == 2:
            logd = "\n".join(
                [
                    logd,
                    f"[{curt}] [ERROR]: {text}"
                ]
            )
            f.write(logd)
            return 0
        
        else:
            return 1
        
log(0, "Starting...")
print("Converting...")

import shutil
import beetroot
import linecache

pb = beetroot.progBar(1)

class InvalidCodecError(Exception):
    pass

def fsort(a):
    ex = "." + a[0].split(".")[-1]
    for i in range(0, len(a)):
        try:
            a[i] = int(".".join(a[i].split(".")[:-1]))
            
        except ValueError:
            raise InvalidCodecError("One of the frames has an invalid name.")
        
    a = sorted(a)
    for i in range(0, len(a)):
        a[i] = str(a[i]) + ex
        
    return a

try:
    if __name__.endswith("__main__"):
        1/0
    
except Exception as error:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    
    perr = type(error).__name__ + ": " + str(error)
    err = f"File {tb.tb_frame.f_locals.get('filename')}: Line {lineno}: " + type(error).__name__ + ": " + str(error)
    log(2, err)
    log(1, "Exiting...")
    print(f"An error has occured.\n{perr}\nCheck `latest.log` for more details.")
    sys.exit()