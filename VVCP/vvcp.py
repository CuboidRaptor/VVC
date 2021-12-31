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
print("Starting...")

import shutil
import beetroot
import linecache
import argparse
import tempfile
import platform

tmpdir = tempfile.gettempdir() if platform.system() == ("Windows" or "Linux") else 1

if platform.system() == "Windows":
    tmpdir += "\\VVCP"
    
elif platform.system() == "Linux":
    tmpdir += "/VVCP"

else:
    raise OSError("Only Windows and Linux are supported")

pb = beetroot.progBar(4)

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
        pa = argparse.ArgumentParser(
            description="Play .vvc files."
        )
        pa.add_argument(
            "File",
            metavar="file",
            type=str,
            help="Filename of .vvc to play"
        )
        args = pa.parse_args()
        file = args.File #The .mp4 file
        vidname = ".".join(file.split(".")[:-1])
        
        log(0, f"The tmpdir is at {tmpdir}")
        log(0, f"File: {file}")
        log(0, "Unpacking...")
        pb.progress()
        ltimer = beetroot.stopwatch()
        wtimer = beetroot.stopwatch()
        ltimer.start()
        
        shutil.unpack_archive(file, tmpdir, "xztar")
        
        pb.progress()
        log(0, f"Done in ~{ltimer.stop()} ms.")
        log(0, f"Display frames")
        ltimer.start()
        
        pb.progress()
        log(0, f"Done in ~{ltimer.stop()} ms.")
        log(0, f"Removing temporary video files")
        ltimer.start()
        
        try:
            shutil.rmtree(tmpdir)
            
        except FileNotFoundError:
            log(1, "File not found when deleting temporary unpacked video.")
            
        except PermissionError:
            log(1, "Permission denied when cleaning up temporary unpacked video.")
        
        pb.progress()
        log(0, f"Done in {ltimer.stop()} ms.")
        
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