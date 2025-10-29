import time

from pyOptoSigma.pyOptoSigma import Controllers, Session, Stages


def main():
    stages = Session(Controllers.SHOT_304GS, verbose_level=3)
    stages.append_stage(Stages.SGSP46_800)

    try:
        stages.connect(portname="COM5")
        stages.initialize()
        stages.set_speed(1, 1000, 10000, 500)
        stages.move(amount=100000, wait_for_finish=True)
        stages.move(amount=200000, wait_for_finish=True, absolute=True)
        stages.set_origin()
        stages.jog()
        time.sleep(10)
        stages.stop()
        stages.get_position()
        stages.reset(wait_for_finish=True)
        stages.move(amount=-200000, wait_for_finish=True, absolute=True)
    finally:
        if stages.connected:
            stages.port.close()


if __name__ == "__main__":
    main()
