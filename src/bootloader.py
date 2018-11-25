###
# Summary: it starts the bps Project
# Parameters: none
# Return: --
###

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import sys
import time

import NAO_main

from optparse import OptionParser

NAO_IP = "10.12.18.236"

memory = None
bootloadr = None
main = None


class Bootloader(ALModule):
    """
    classdocs
    """

    def __init__(self, name):
        ###
        # Summary: it starts the load of all modules
        # Parameters: self, name of the module to initialize
        # Return: --
        ###

        ALModule.__init__(self, name)

        self.tts = ALProxy("ALTextToSpeech")
        global memory
        global main
        main = NAO_main
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("MiddleTactilTouched", "bootloadr", "onTouched")

    def onTouched(self, *_args):
        ###
        # Summary: called when head is touched
        # Parameters: self, args in case there are arguments
        # Return: --
        ###


        memory.unsubscribeToEvent("MiddleTactilTouched", "bootloadr")
        # Nao says Start Scoccer
        self.tts.say("Start soccer")
        # subscribe to these events
        memory.subscribeToEvent("MiddleTactilTouched", "bootloadr", "onSecondTouch")
        # start main function
        main.start()

    def onSecondTouch(self, *_args):
        ###
        # Summary: called when head is touched again
        # Parameters: self, args in case there are arguments
        # Return:
        ###

        memory.unsubscribeToEvent("MiddleTactilTouched", "bootloadr")
        # Nao says Stop
        self.tts.say("STOP")
        # stop the main execution
        main.stop()
        # subscribe to these events
        memory.subscribeToEvent("MiddleTactilTouched", "bootloadr", "onTouched")


def main():
    ###
    # Summary: main execution method
    # Parameters: --
    # Return: --
    ###

    parser = OptionParser()
    parser.add_option("--pip", help="Parent broker port. The IP address or your robot", dest="pip")
    parser.add_option("--pport", help="Parent broker port. The port NAOqi is listening to", dest="pport", type="int")
    parser.set_defaults(pip=NAO_IP, pport=9559)

    (opts, args_) = parser.parse_args()
    pip = opts.pip
    pport = opts.pport

    myBroker = ALBroker("myBroker", "0.0.0.0", 0, pip, pport)

    global bootloadr
    bootloadr = Bootloader("bootloadr")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()


