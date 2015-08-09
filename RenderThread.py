from multiprocessing import Process, Pool
from multiprocessing.managers import BaseManager
import tempfile
import subprocess
import threading 
import time
import os
import json 
import signal

def writeJobData(uuid):
    config = {}
    config['output-uuid'] = uuid
    config['samples'] = 20
    config['volume_step_size'] = 0.2
    config['sample_clamp_direct'] = 9
    config['sample_clamp_indirect'] = 9
    config['caustics_reflective'] = False
    config['max_bounces'] = 128
    config['transparent_max_bounces'] = 128
    config['diffuse_bounces'] = 3
    config['glossy_bounces'] = 3
    config['volume_bounces'] = 3
    config['transmission_bounces'] = 128
    config['shading_system']= False
    config['debug_use_spatial_splits'] = False
    config['use_persistent_data'] = False
    config['file_format'] = 'JPEG'
    
    with open(uuid + '.json', 'w') as f:
        json.dump(config, f)

class blender_thread(threading.Thread):
    def __init__(self, threadID, name, cmd):
        super(blender_thread, self).__init__()
        self.setDaemon = False
        self.ct = threading.currentThread()
        self.threadID = threadID
        self.name = name
        self.cmd = cmd
        self.finished = threading.Event()
        
    def run(self):
        threadLock.acquire()
        outs,errs = render(self.cmd, self.name)
        threadLock.release()

exitFlag = 0
threadLock = threading.Lock()
threads = []

def render(cmd, uuid):
    # os.path.join(o, filename)
    writeJobData(uuid)
    process = subprocess.Popen(cmd) #,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE
    try:
        outs, errs = process.communicate(timeout=1)
    except Exception:
        process.kill()
        outs, errs = process.communicate()
    if exitFlag:
        thread.exit()
    time.sleep(.5)
    print("%s: %s" % (uuid, time.ctime(time.time())))
    return (outs,errs)
    
def runJob(uuid):
    args = "E:/BIN/blender/blender-2.75-33bac1f-win64/blender.exe --background %s.blend -noglsl -noaudio --python dorender.py -- %s" % (uuid,uuid)
    T = blender_thread(0, uuid, args)
    T.start()
    T.join()

uuid='0000-0000-0000'
runJob(uuid)