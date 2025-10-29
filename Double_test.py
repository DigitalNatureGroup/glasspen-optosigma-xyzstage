import pyOptoSigma
from pyOptoSigma import *
import time

stages = Session(Controllers.SHOT_304GS)
stages.append_stage(Stages.OSMS26_100)
stages.append_stage(Stages.OSMS26_100)
stages.connect(portname='COM8')

while True:
    print("start")
    print(stages.stages)
    stages.move(stage=1, amount=1000, wait_for_finish=False)
    time.sleep(0.00001) # これがないとbad timingが出る
    stages.move(stage=2, amount=1000, wait_for_finish=False)