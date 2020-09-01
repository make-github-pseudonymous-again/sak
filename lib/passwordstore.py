import subprocess

def get ( key ) :

    p = subprocess.run(['pass', key], stdout=subprocess.PIPE)
    rc = p.returncode

    if rc == 0 : return p.stdout.decode('utf-8')[:-1]

    message = p.stderr.decode('utf-8')
    error = '"pass {}" returned {}: {}'.format(key, rc, message)
    raise Exception(error)
