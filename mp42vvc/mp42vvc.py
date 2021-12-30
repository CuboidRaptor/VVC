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
import platform

from moviepy.editor import VideoFileClip

pb = beetroot.progBar(5)

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
        curdir = os.path.abspath(sys.argv[0])
        vtracer = (os.path.dirname(curdir) + "\\vtracer.exe") if platform.system() == "Windows" else ((os.path.dirname(curdir) + "/vtracer") if platform.system() == "Linux" else 1)
        
        if vtracer == 1:
            raise OSError("Only Windows and Linux are supported.")
        
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
        vidname = ".".join(file.split(".")[:-1])
        
        try:
            os.mkdir(vidname)
            
        except FileExistsError:
            pass
        
        if not file.endswith(".mp4"):
            class FileError(Exception):
                pass
            
            raise FileError("The entered file isn't an mp4 file")

        log(0, f"File: {file}")
        log(0, "Extracting frames...")
        pb.progress()
        ltimer = beetroot.stopwatch()
        wtimer = beetroot.stopwatch()
        ltimer.start()
        wtimer.start()
        
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
            frame_fname = os.path.join(fname, f"{nam}.jpg")
            vclip.save_frame(frame_fname, current_duration)
            
        log(0, f"Done in ~{ltimer.stop()} ms.")
        log(0, "Converting to Vector graphics...")
        pb.progress()
        ltimer.start()
        
        try:
            fname2 = vidname + "/frames"
            os.mkdir(fname2)
            
        except FileExistsError:
            pass
        
        for item in fsort(os.listdir(fname)):
            with beetroot.suppress():
                subprocess.call(vtracer + f" -f 16 -p 8 -g 0 -m polygon --input {fname}/{item} ---output {fname2}/" + ".".join(item.split(".")[:-1] + ["svg"]))
            
        log(0, f"Done in ~{ltimer.stop()} ms.")
        log(0, "Removing temporary frame folder...")
        pb.progress()
        ltimer.start()
        
        try:
            shutil.rmtree(fname)
            #pass
            
        except FileNotFoundError:
            log(1, "File not found when deleting temporary .bmp folder for frame extracts")
            
        except PermissionError:
            log(1, "Either permission is not granted or frames are being accessed by another program.")
            
        log(0, f"Done in ~{ltimer.stop()} ms.")
        log(0, "Demuxing audio...")
        pb.progress()
        ltimer.start()
        
        vclip.audio.write_audiofile(vidname + "/audio.wav", codec="pcm_s16le")
            
        pb.progress()
        print("\nDone!")
        log(0, f"Done in ~{ltimer.stop()} ms.\n")
        log(0, f"MP42VVC is done! It took {wtimer.stop()} ms.")
    
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