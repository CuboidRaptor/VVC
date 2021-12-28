#Imports
import argparse

pa = argparse.ArgumentParser(
    description="Convert .mp4s to .vvcs."
)
pa.add_argument(
    "File",
    metavar="f",
    type=str,
    help="Filename of .mp4 to be converted"
)
args = pa.parse_args()
file = args.File
print(file)