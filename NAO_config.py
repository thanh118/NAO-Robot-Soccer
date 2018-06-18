###
# Summary: used to load all Proxy Modules and initial configurations 
# Parameters: none 
# Return: messages about the load, if it successes or failed or which proxys were loaded
###   


from naoqi import ALProxy


class Config:
    # default IP
    IP = "10.12.18.236"
    # default Port
    PORT = 9559

    def __init__(self, logger):

        # initialize logger atribute
        self.logger = logger

        # send information to logger indicating config class is initializes and proxys are open
        logger.info("Config-Class initialized")
        logger.info("Opening Proxys at: " + str(self.IP) + ":" + str(self.PORT))
        try:
            # try to start AlMotion proxy and send info to logger
            self.motionProxy = ALProxy("ALMotion", self.IP, self.PORT)
            logger.info("ALMotion loaded")
        except RuntimeError:
            # in case of error, send information to logger
            self.throw(logger, "Unable to connect to MotionProxy")
        try:
            # try to start AlTextToSpeech proxy and send info to logger
            self.speechProxy = ALProxy("ALTextToSpeech", self.IP, self.PORT)
            logger.info("ALTextToSpeech loaded")
        except RuntimeError:
            # in case of error, send information to logger
            self.throw(logger, "Unable to connect to SpeechProxy")
        try:
            # try to start AlBehaviorManager proxy and send info to logger
            self.behaviorProxy = ALProxy("ALBehaviorManager", self.IP, self.PORT)
            logger.info("ALBehaviorManager loaded")
        except RuntimeError:
            # in case of error, send information to logger
            self.throw(logger, "Unable to connect to BehaviorProxy")
        try:
            # try to start AlRedBallTracker proxy and send info to logger
            self.redBallProxy = ALProxy("ALRedBallTracker", self.IP, self.PORT)
            logger.info("ALRedBallTracker loaded")
        except RuntimeError:
            # in case of error, send information to logger
            self.throw(logger, "Unable to connect to ALRedBallTracker")
        try:
            # try to start AlVideoDevice proxy and send info to logger
            self.videoProxy = ALProxy("ALVideoDevice", self.IP, self.PORT)
            logger.info("ALVideoDevice loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALVideoDevice")
        try:
            # try to start AlRedBallDetection proxy and send info to logger
            self.redBallDetection = ALProxy("ALRedBallDetection", self.IP, self.PORT)
            logger.info("ALRedBallDetection loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALRedBallDetection")
        try:
            # try to start AlMemory proxy and send info to logger
            self.memory = ALProxy("ALMemory", self.IP, self.PORT)
            logger.info("ALMemory loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALMemory")
        try:
            # try to start AlPosture proxy and send info to logger            
            self.posture = ALProxy("ALRobotPosture", self.IP, self.PORT)
            logger.info("ALRobotPosture loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALRobotPosture")
        try:
            # try to start AlNavigation proxy and send info to logger            
            self.navigation = ALProxy("ALNavigation", self.IP, self.PORT)
            logger.info("ALNavigation loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALNavigation")
        try:
            # try to start AlSonar proxy and send info to logger        
            self.sonar = ALProxy("ALSonar", self.IP, self.PORT)
            logger.info("ALSonar loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALSonar")
        try:
            # try to start AlSensors proxy and send info to logger            
            self.sensors = ALProxy("ALSensors", self.IP, self.PORT)
            logger.info("ALSensors loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALSensors")
        try:
            # try to start AlProxy proxy and send info to logger
            self.naoMarkProxy = ALProxy("ALLandMarkDetection", self.IP, self.PORT)
            logger.info("ALLandMarkDetection loaded")
        except RuntimeError:
            # in case of error, send information to logger            
            self.throw(logger, "Unable to connect to ALLandMarkDetection")

    def throw(self, logger, message):
        ###
        # Summary: send the message passed by parameters to logger class in case of fatal error
        # Parameters: self, logger, message we want to write into logger
        # Return: message in logger class
        ###
        logger.fatal(message)

    def getProxy(self, proxy):
        ###
        # Summary: get the information inside a proxy
        # Parameters: self and the proxy we want information about
        # Return: information about the data inside the proxy or a fatal message into logger
        ###
        # write information in logger about the proxy which is trying to hand over
        self.logger.info("Trying to hand over " + proxy)
        # check which one is the proxy passed by parameters
        if (proxy is "ALMotion"):
            return self.motionProxy
        elif (proxy is "ALTextToSpeech"):
            return self.speechProxy
        elif (proxy is "ALBehaviorManager"):
            return self.behaviorProxy
        elif (proxy is "ALRedBallTracker"):
            return self.redBallProxy
        elif (proxy is "ALVideoDevice"):
            return self.videoProxy
        elif (proxy is "ALRedBallDetection"):
            return self.redBallDetection
        elif (proxy is "ALMemory"):
            return self.memory
        elif (proxy is "ALRobotPosture"):
            return self.posture
        elif (proxy is "ALNavigation"):
            return self.navigation
        elif (proxy is "ALSonar"):
            return self.sonar
        elif (proxy is "ALSensors"):
            return self.sensors
        elif (proxy is "ALLandMarkDetection"):
            return self.naoMarkProxy
        else:
            # in case it can not recognize the proxy, it will return a fatal message to logger class
            self.logger.fatal("Could not find " + proxy)
            return 0

    def getIP(self):
        ###
        # Summary: get the IP
        # Parameters:self
        # Return: IP
        ###
        return self.IP

    def getPort(self):
        ###
        # Summary: get the Port
        # Parameters: self
        # Return: Port
        ###
        return self.PORT