#Dependencies (to pip install):
#moviepy
#pypotrace

#function things

import datetime

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

with open("latest.log", "w") as f:
    pass

def log(mode, text):
    #logger ig
    with open("latest.log", "r") as f:
        logd = f.read()
    
    with open("latest.log", "w") as f:
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

#Imports
import argparse
import numpy as np
import os
import sys
import traceback
import linecache
import subprocess
import beetroot
import shutil

from moviepy.editor import VideoFileClip

pb = beetroot.progBar(4)

def fsort(a):
    ex = "." + a[0].split(".")[-1]
    for i in range(0, len(a)):
        a[i] = int(".".join(a[i].split(".")[:-1]))
        
    a = sorted(a)
    for i in range(0, len(a)):
        a[i] = str(a[i]) + ex
        
    return a

try:
    if __name__.endswith("__main__"):
        #Argparse stuff
        pa = argparse.ArgumentParser(
            description="Convert .mp4s to .vvcs."
        )
        pa.add_argument(
            "File",
            metavar="file",
            type=str,
            help="Filename of .mp4 to be converted"
        )
        args = pa.parse_args()
        file = args.File #The .mp4 file

        log(0, f"File: {file}")
        log(0, "Extracting frames...")
        pb.progress()
        
        vclip = VideoFileClip(file)
        fname = "tempframes"
        
        try:
            os.mkdir(fname)
            
        except FileExistsError:
            pass
        
        sfps = vclip.fps
        
        log(0, f"Video fps: {sfps}")
        
        step = 1 / vclip.fps if sfps == 0 else 1 / sfps
        
        nam = -1
        for current_duration in np.arange(0, vclip.duration, step):
            nam += 1
            frame_fname = os.path.join(fname, f"{nam}.bmp")
            vclip.save_frame(frame_fname, current_duration)
            
        log(0, "Converting to Vector graphics...")
        pb.progress()
        
        curdir = os.path.abspath(sys.argv[0])
        
        try:
            fname2 = "frames"
            os.mkdir(fname2)
            
        except FileExistsError:
            pass
        
        for item in fsort(os.listdir(fname)):
            with beetroot.suppress():
                subprocess.call(os.path.dirname(curdir) + f"/potrace/potrace.exe tempframes/{item} -s --group -o frames/" + ".".join(item.split(".")[:-1] + ["svg"]))
            
        log(0, "Removing temporary frame folder...")
        pb.progress()
        
        try:
            shutil.rmtree(fname)
            
        except FileNotFoundError:
            log(1, "File not found when deleting temporary .bmp folder for frame extracts")
            
        except PermissionError:
            log(1, "Either permission is not granted or frames are being accessed by another program.")
            
        pb.progress()
        print("\nDone!")
    
except Exception as error:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    
    err = f"Line {lineno}: " + type(error).__name__ + ": " + str(error)
    log(2, err)
    log(1, "Exiting...")
    print(f"An error has occured.\n{err}\nCheck `latest.log` for more details.")
    sys.exit()