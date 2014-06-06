import os.path
import glob

TASK_PATH = os.path.dirname(__file__)

def available():
    cmds = [ "\t" + os.path.basename(f)[:-3] for f in glob.glob(TASK_PATH + '/[a-z]*.py') ]
    return "\n".join(cmds)
