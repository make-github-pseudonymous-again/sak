import os
import subprocess

PATH = "PATH"
PATH_SEP = os.pathsep
BIN = "bin"

pathlist = os.getenv(PATH).split(PATH_SEP)

froot = os.path.dirname(__file__)

fbin = os.path.join(froot, BIN)

if fbin not in pathlist:
    subprocess.call(["setx", PATH, fbin])
