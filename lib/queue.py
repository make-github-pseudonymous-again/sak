
import lib.sys , subprocess

CMD_QSUB = "qsub"
CMD_QDEL = "qdel"
CMD_QSTAT = "qstat"

KEY_JOB_NAME = "Job_Name"
KEY_JOB_STATE = "job_state"
KEY_JOB_OWNER = "Job_Owner"

STATE_COMPLETED = "C"
STATE_QUEUED = "Q"
STATE_RUNNING = "R"

def submit ( node , cpu , name , out , err , *cmd ) :

	"""
		qsub python wrapper
	"""

	resources = {"nodes" : node + ":ppn=" + str(cpu)}

	resource_list = ",".join(["=".join([key, val]) for key, val in resources.iteritems()])

	submission = [CMD_QSUB, "-l", resource_list, "-N",  name, "-o",  out, "-e",  err]

	cmd = [ [ "echo" ] + [ " ".join( cmd ) ] , submission ]

	return lib.sys.pipeline(*cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE)



def delete ( queueid ) :

	"""
		qdel python wrapper
	"""

	return lib.sys.call( [ CMD_QDEL , str( queueid ) ] )


def splitowner ( owner ) :

	return owner.split( "@" )


def stat ( ) :

	"""
		qstat python wrapper
	"""

	out, err, p = lib.sys.call( [ CMD_QSTAT , "-f" ] )

	if lib.sys.failure( p ) or not out : return { }

	stat = { }
	current = None

	N_SPACES = 4

	for line in out.decode( ).splitlines( ) :

		if not line : continue

		if line[0] == "\t" :
			current[key] += line[1:]

		elif line[:N_SPACES] == " " * N_SPACES :
			key, part = line[N_SPACES:].split(" = ")
			current[key] = part

		elif line[:8] == "Job Id: ":
			jobid = line[8:]
			stat[jobid] = {}
			current = stat[jobid]

	return stat
