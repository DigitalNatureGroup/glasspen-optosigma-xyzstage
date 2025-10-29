import pyOptoSigma
from pyOptoSigma import *
import time

stages = Session(Controllers.SHOT_304GS)
stages.append_stage(Stages.OSMS26_100)
stages.connect(portname='COM5')

while True:
    print("s")
    start_time = time.time()
    stages.move(amount=1000, wait_for_finish=False)
    end_time = time.time()
    elasped_time = end_time - start_time
    print(elasped_time)
    time.sleep(1.0-elasped_time)
    