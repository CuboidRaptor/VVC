#function things

import datetime
import traceback

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

#Imports
import argparse
import numpy as np
import os
import sys

from datetime import timedelta
from moviepy.editor import VideoFileClip

#Argparse stuff
try:
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
    
    1/0

except Exception as error:
    log(2, str(traceback.format_exc()).replace("\n", " "))
    log(1, "Exiting...")
    sys.exit()