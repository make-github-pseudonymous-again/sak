import subprocess


def release():

    subprocess.call(["python3", "setup.py", "sdist", "upload"])
