
import os.path

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
BIN = os.path.join(ROOT, "bin")
LIB = os.path.join(ROOT, "lib")
SAK = os.path.join(ROOT, "sak")
DATA = os.path.join(ROOT, "data")

def data(*path):
	return os.path.join(DATA, *path)
