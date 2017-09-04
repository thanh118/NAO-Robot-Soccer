###
# Summary: this class will handle all the motions in the robot
# Parameters: none
# Return: --
###
import math


class Motion:
    def __init__(self, logger, config):
        ###
        # Summary: initialize logger, config and load behaviors
        # Parameters: self, logger and config
        # Return:
        ###

        # use the logger passed by parameters
        self.logger = logger
        # use the config passed by parameters
        self.config = config
        # get proxys of AlBehaviorManager, AlMotion and AlRobotPosture
        self.behaviorManager = self.config.getProxy("ALBehaviorManager")
        self.motion = self.config.getProxy("ALMotion")
        self.posture = self.config.getProxy("ALRobotPosture")
        # write into logger
        logger.info("Motion-Class initialized")

    def run(self, behaviorName):
        ###
        # Summary: execute a behavior in case this is already installed, if not, give us a warn
        #         message saying "behavior XXX is not installed"
        # Parameters: self, behavior Name which is the name of the behavior we want to run
        # Return: --
        ###

        # write into logger
        self.logger.info("Trying to run Behavior: " + behaviorName)
        # if behavior is already installed...
        if (self.behaviorManager.isBehaviorInstalled(behaviorName)):
            # change the stiffness in Nao
            self.changeStiffness(1.0)
            # write into logger
            self.logger.info("Now running Behavior: " + behaviorName)
            # execute the behavior
            self.behaviorManager.runBehavior(behaviorName)
            # write into logger
            self.logger.info("Finished running Behavior: " + behaviorName)
        else:
            # write a warning message into logger
            self.logger.warn("Behavior ", + behaviorName + " is not installed")

    def stop(self):
        ###
        # Summary: stops the execution of all the motion behaviors
        # Parameters: self
        # Return: --
        ###
        # write a message into logger
        self.logger.info("Trying to stop the currently running Behavior: " + str(self.motion.getRunningBehaviors))
        # stop all behaviors in execution
        self.motion.stopAllBehaviors()

    def getBehaviors(self):
        ###
        # Summary: write in a list all the behaviors already installed in the robot
        # Parameters: self
        # Return: --
        ###
        # get the list of behaviors installed
        behaviorList = self.behaviorManager.getInstalledBehaviors()
        # write the list into logger
        self.logger.info("Behaviors on the robot:")
        self.logger.info(str(behaviorList))

    def getRunningBehaviors(self):
        ###
        # Summary: write in a list all the behaviors currently running in the robot
        # Parameters: self
        # Return: --
        ###
        # get the list of running behaviors in that moment
        behaviorList = self.behaviorManager.getRunningBehaviors()
        # write the list into logger
        self.logger.info("Running Behaviors:")
        self.logger.info(str(behaviorList))

    def changeStiffness(self, stiffness):
        ###
        # Summary: change the stiffness in the robot, if it s on changes it to off and viceversa
        # Parameters: self, stiffness will change the stiffness to on or off
        # Return: --
        ###
        # write into logger
        self.logger.info("Changing Stiffness to: " + str(stiffness))
        # change stiffness of the body
        self.motion.setStiffnesses("Body", stiffness)

    def enableBalancer(self):
        ###
        # Summary: turn on body balancer
        # Parameters: self
        # Return: --
        ###
        # write into logger
        self.logger.info("Enabling Body Balancer")
        # change body balancer to true
        self.motion.wbEnable(True)

    def disableBalancer(self):
        ###
        # Summary: turn off body balancer
        # Parameters: self
        # Return: --
        ###
        # write into logger
        self.logger.info("Disable Body Balancer")
        # change the body balancer to false
        self.motion.wbEnable(False)

    def standUp(self):
        ###
        # Summary: the robot will stand up
        # Parameters: self
        # Return: --
        ###
        # execute the method wakeup that make Nao to stand up
        self.motion.wakeUp()
        # take Nao from waking up posture to the indicated StandInit posture
        self.posture.goToPosture("StandInit", 0.7)

    def rest(self):
        ###
        # Summary: the robot will stay in resting position
        # Parameters: self
        # Return: --
        ###
        # Nao will be in resting position
        self.motion.rest()

    def moveTo(self, x, y, theta):
        ###
        # Summary: make the robot move to (x,y) with the angle theta
        # Parameters: self, x and y are the position in the space and theta is the angle till that position
        # Return: --
        ###
        # write into logger
        self.logger.info("Starting to walk to: " + str(x) + "," + str(y) + " with " + str(theta))
        # Nao will move till position (x,y) with an angle theta
        self.motion.moveTo(x, y, theta)

    def turnHead(self, degree, time):
        ###
        # Summary: Nao moves its head expressed in degree and time
        # Parameters: self, degree indicate how many degrees Nao will move its head and time indicates
        #                in how much time it will do that movement.
        # Return:
        ###
        # write into logger
        self.logger.info("Turning Head to: " + str(degree))
        # -2/2
        # if head is between these degrees, then Nao can move its head
        if ((degree >= -118) & (degree <= 118)):
            self.motion.angleInterpolation(
                ["HeadYaw"],
                [math.radians(degree)],
                [time],
                True
            )
        # else, write warning message into logger
        else:
            self.logger.warn("Could not turn head")

    def pitchHead(self, degree, time):
        ###
        # Summary: Nao pitches its head expressed in degree and time
        # Parameters: self, degree indicate how many degrees Nao will move its head and time indicates
        #                in how much time it will do that movement.
        # Return:
        ###
        # write into logger
        self.logger.info("Pitching Head to: " + str(degree))
        # -2/2
        # if head is between these degrees, then Nao can move its head
        if ((degree >= -30) & (degree <= 22)):
            self.motion.angleInterpolation(
                ["HeadPitch"],
                [math.radians(degree)],
                [time],
                True
            )
        else:
            # else, write warning message into logger
            self.logger.warn("Could not pitch head")

    def getUp(self):
        ###
        # Summary: load the behavior bps_GetUp and Nao will get up
        # Parameters: self
        # Return: --
        ###
        # execute behavior GetUp
        self.run("bps_GetUp")

    def getDown(self):
        ###
        # Summary: load the behavior bps_GetDown and Nao will get down
        # Parameters: self
        # Return: --
        ###
        # execute behavior GetDown
        self.run("bps_GetDown")

    def getSensorValue(self, sensorName):
        ###
        # Summary: get the value of the angle of a sensor in Nao
        # Parameters: self, sensorName indicate the name of a sensor from which we want to get
        #            information about the angles
        # Return: angles in the sensor indicated in sensorName
        ###
        return self.motion.getAngles(sensorName, False)

    def getRobotPosition(self):
        ###
        # Summary: it gives us the position of Nao
        # Parameters: self
        # Return: position of Nao
        ###
        # write message in logger
        self.logger.info("Current robot position: " + str(self.motion.getRobotPosition(False)))
        # return the position of the robot
        return self.motion.getRobotPosition(False)

    def getRobotVelocity(self):
        ###
        # Summary: it gives us the velocity of Nao
        # Parameters: self
        # Return: the velocity of Nao
        ###
        # write information into logger
        self.logger.info("Current velocity: " + str(self.motion.getRobotVelocity()))
        # return the velocity of Nao
        return self.motion.getRobotVelocity()

    def setWalkTargetVelocity(self, x, y, theta, freq):
        ###
        # Summary: it sets the velocity to the position indicated in (x,y) with the angle theta
        # Parameters: self, x and y are the position in the space, theta the angle till that position
        #            and freq is the velocity
        # Return: --
        ###
        # set the velocity of Nao till one point in the space
        self.motion.setWalkTargetVelocity(x, y, theta, freq)

    def stopEverything(self):
        ###
        # Summary: Nao will stop moving
        # Parameters: self
        # Return: --
        ###
        # write information into logger
        self.logger.info("Stoping Movement")
        # stop any movement
        self.motion.stopMove()

    def turnAround(self, degree):
        ###
        # Summary: Noa will turn around the degrees indicated in degree
        # Parameters: self, degree indicate how many degrees Nao will be moved
        # Return: --
        ###
        self.logger.info("Trying to turn around " + str(degree) + "dg")
        # calculate the angle
        theta = math.radians(degree)
        # move Nao till that position
        self.moveTo(0, 0, theta)

    def placeBall(self):
        ###
        # Summary: it loads the behavior bps_PlaceBall which try to place the ball on the floor
        # Parameters: self
        # Return: --
        ###
        # execute behavior PlaceBall
        self.run("bps_PlaceBall")

    def openLeftHand(self):
        ###
        # Summary: it will open Nao s left hand
        # Parameters: self
        # Return: --
        ###
        # close: 0.01
        # open: 0.98
        self.motion.angleInterpolation(
            ["LHand"],
            [0.98],
            [0.5],
            True)

    def closeLeftHand(self):
        ###
        # Summary: it will close Nao s left hand
        # Parameters: self
        # Return: --
        ###
        # close: 0.01
        # open: 0.98
        self.motion.angleInterpolation(
            ["LHand"],
            [0.01],
            [0.5],
            True)

    def openRightHand(self):
        ###
        # Summary: it will open Nao s right hand
        # Parameters: self
        # Return: --
        ###
        # close: 0.01
        # open: 0.98
        self.motion.angleInterpolation(
            ["RHand"],
            [0.98],
            [0.5],
            True)

    def closeRightHand(self):
        ###
        # Summary: it will close Nao s right hand
        # Parameters: self
        # Return: --
        ###
        # close: 0.01
        # open: 0.98
        self.motion.angleInterpolation(
            ["RHand"],
            [0.01],
            [0.5],
            True)

    def closeBothHands(self):
        ###
        # Summary: it will close Nao s hands
        # Parameters: self
        # Return: --
        ###
        # it calls both methods for closing hands
        self.closeRightHand()
        self.closeLeftHand()

    def kickBall(self):
        ###
        # Summary: it will execute Kick behavior
        # Parameters: self
        # Return: --
        ###
        self.run("bps_Kick")

    def rotateAroundBall(self, distance, angle):
        ###
        # Summary: Nao will rotate around the ball
        # Parameters: self, distance to ball, angle of rotation
        # Return: --
        ###
        # write information about rotation into logger
        self.logger.info("Rotating around ball at distance " + str(distance) + " / " + str(angle) + " degrees")
        # calculate position and radians till the ball
        x = distance - math.cos(math.radians(angle)) * 0.25
        y = math.sin(math.radians(angle)) * distance
        theta = math.radians(angle)
        # move to position indicated in (x,y) with the angle theta
        self.moveTo(x, -y, theta)


    def celebrateGoal(self):
        ###
        # Summary: execute Victory behavior
        # Parameters: self
        # Return: --
        ###
        self.run("bps_Victory")

    def grabBall(self, number):
        ###
        # Summary: Nao grabs the ball according to where is the ball
        # Parameters: self, number indicate in which area is the ball. There are 3 established areas
        # Return: --
        ###
        self.logger.info("Picking up at: " + str(number))
        if (number == 0):
            self.run("bps_Pick_Field0")
            return 1
        if (number == 1):
            self.run("bps_Pick_Field1")
            return 1
        if (number == 2):
            self.run("bps_Pick_Field2")
            return 1