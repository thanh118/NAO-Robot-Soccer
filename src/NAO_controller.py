"""
# Summary: controller class for the general line of execution
# Parameters: none
# Return: --
"""
import NAO_motion
import NAO_sensor
import time
import math
import motion

class Controller():
    
    def __init__(self, logger, config):
       
    ###
    # Summary: main method for setting up proxys and variables
    # Parameters: self, logger in which we will write all the important messages and config to
    #              activate all the configurations
    # Return: --
    ###

        # We initialize Controller Class
        logger.info("Controller-Class initialized")
        
        self.logger = logger
        self.config = config
        self.motion = NAO_motion.Motion(logger, config)
        self.sensor = NAO_sensor.Sensor(logger, config)
        self.speech = config.getProxy("ALTextToSpeech")
        
        #How close Nao will try to get to the ball in meters(>0.25)
        self.distanceToTarget = 0.27
        #How many times the ball can be out of sight before Nao stops
        self.ballLostMax = 10 
        #Time the head movement stops for ball recognition
        self.retardSecond = 2
        #Nao walking speed 0.0 to 1.0
        self.walkingSpeed = 0.3
        #An obstacle ahead, lower than this value will cause Nao to stop 
        self.maxSonar = 0.3 
        #Time the thread sleeps for the next walking iteration in seconds
        self.walkIterationTime = 0.05
        self.rotations = 0
        self.isStop = False
        self.firstIteration = True
        
    def start(self):       
    ###
    # Summary: start method with general setup calls
    # Parameters: self
    # Return: 1 if its stoped
    ###
        
        if (self.isStop):
            self.end()
            return 1
        
        self.logger.info("Controller: Starting...")
        
        self.motion.getBehaviors()
        #The maximum volume of text-to-speech outputs
        self.speech.setVolume(0.5) 
        
        self.speech.say("Standing up")
        self.motion.standUp()
        
        # We need to close the hands here, because Nao sometimes opens them after standing up
        self.motion.closeBothHands()
        
        # stop head tracking
        self.sensor.stopHeadTracker()
                
        self.lookForBallCloseRange()
        
    def lookForBallCloseRange(self):
    ###
    # Summary: used to look for the red ball in close range (0.2-1.2m)
    # Parameters: self
    # Return: 1 if its stopped
    ###    
        
        if (self.isStop):
            self.end()
            return 1
        
        
        self.speech.say("Looking short")
        # activate camera, 0top 1bottom
        self.sensor.setCamera(1)
        self.sensor.subscribeToRedball()

        #Look for the ball straight ahead
        
        if(self.firstIteration):
            time.sleep(2)
            self.firstIteration = False

        if (self.sensor.isNewBall()):
            # New Ball found
            self.ballFound()
            return 1
        #Look for the ball on the left
        self.motion.turnHead(30, 0.5) 
        time.sleep(self.retardSecond)
        if(self.sensor.isNewBall()):
            #New Ball found          
            self.motion.turnAround(30)
            self.ballFound()
            return 1
        
        #Look for the ball on the right       
        self.motion.turnHead(-30, 0.5)     
        time.sleep(self.retardSecond)
        if(self.sensor.isNewBall()):
            #New Ball found   
            self.motion.turnAround(-30)
            self.ballFound()
            return 1


        #"Could not find my ball" message    
        self.speech.say("Could not find my ball")
        self.sensor.unsubscribeToRedBall()
        
        if(self.rotations != 5):
            #Recursion
            # moving head
            self.motion.turnHead(0, 0.1)
            # moving body
            self.motion.turnAround(60)
            # rotating robot
            self.rotations = self.rotations + 1
            self.lookForBallCloseRange()
        else:
            self.end()
        
            
            
    def ballFound(self):    
    ###
    # Summary: Called when the ball has been found
    # Parameters: self
    # Return: 1 if it s stopped
    ###    
        
        if (self.isStop):
            self.end()
            return 1
        
        #"I found my ball" message 
        self.speech.say("I found my ball")
        
        self.rotations = 0
        # move head
        self.motion.turnHead(0, 0.5) 
        # Nao walks to ball
        self.walkToBall()
        


    def walkToBall(self):
    ###
    # Summary: Used to walk to the red ball target
    # Parameters: self
    # Return: 1 if it s stopped
    ###        
        
        if (self.isStop):
            self.end()
            return 1

        #"Looking at my ball" message 
        self.speech.say("Looking at my ball")
        
        ballLost = 0
        atBall = False
        
        #Starting the sensors 
        self.sensor.startHeadTracker()
        self.sensor.startSonar()
        
        while(atBall == False):
            if (self.isStop):
                self.sensor.stopHeadTracker()
                self.sensor.stopSonar()
                self.end()
                return 1
            
            time.sleep(self.walkIterationTime)
            
            headAngle = self.motion.getSensorValue("HeadYaw")[0]
            
            #Check whether or not we are looking at our own shoulders
            if(headAngle < - 0.75 or headAngle > 0.75):
                self.logger.info("HeadYaw: " + str(headAngle))
                self.sensor.stopHeadTracker()
                self.motion.turnHead(0.0, 0.5)
                self.sensor.startHeadTracker()
            
            # get the ball position
            x = self.sensor.getBallPosition()[0]
            y = self.sensor.getBallPosition()[1]
            
            self.distance = math.sqrt(math.pow(x,2)+math.pow(y,2))
            angle = math.atan2(y, x)
            angleRounded = int(angle/(5.0*motion.TO_RAD))*(5.0*motion.TO_RAD)
            
            #The walking velocity angle must be between -1 and 1
            if(angleRounded>1):
                angleRounded = 1
            if(angleRounded<-1):
                angleRounded = -1
            
            self.logger.info("Ball at: " + str(x) + "," + str(y) + " with " + str(angleRounded) + " in " + str(self.distance))
            
            #Reducing the speed the closer we get to the ball
            speed = self.walkingSpeed
            if(self.distance <= self.walkingSpeed):
                speed = self.distance   
            
            #Actual walking call (non blocking and iterated)
            self.motion.setWalkTargetVelocity(1.0, 0.0, angleRounded, speed)
            
            #Checking if the ball is still visible
            if(self.sensor.isNewBall() == False):
                ballLost = ballLost + 1
                self.logger.info("Ball lost?")
            else:
                ballLost = 0
                
            #Collision detection and reaction
            self.colLeft = False
            self.colRight = False
            
            if(self.sensor.getSonarLeft() <= self.maxSonar):
                self.colLeft = True
                
            if(self.sensor.getSonarRight() <= self.maxSonar):
                self.colRight = True
                
            self.tooClose(self.colLeft, self.colRight)
                
            #If we lost sight of the ball a certain amount  
            if(ballLost >= self.ballLostMax):
                self.speech.say("I lost track of my ball")
                atBall = True
                self.motion.stopEverything()
                self.sensor.stopHeadTracker()
                self.sensor.stopSonar()
                self.motion.standUp()
                self.lookForBallCloseRange()
                return 1
            
            #If we reached our target distance
            if(self.distance <= self.distanceToTarget):
                self.logger.info("At my Target")
                self.motion.stopEverything()
                self.sensor.stopHeadTracker()
                atBall = True
                
                self.motion.standUp()
        
                self.speech.say("Final correction")
                self.motion.turnAround(math.degrees(angle))
                
                self.sensor.stopSonar()
                self.findGoal()
                return 1        
                
    def pickUpBall(self):    
    ###
    # Summary: Picking up the ball
    # Parameters: self
    # Return: 1 if it s stopped
    ###  
        
        if (self.isStop):
            self.end()
            return 1
        
        # stop head tracker
        self.sensor.stopHeadTracker()

        self.motion.standUp()
        self.motion.closeBothHands()
        
        self.motion.getDown()
        self.motion.openRightHand()
        # moving head
        self.motion.pitchHead(0, 0.4)
        self.motion.turnHead(0, 0.4)
        # start head tracking
        self.sensor.startHeadTracker()
        
        self.speech.say("Calculating ball position")
            
        time.sleep(1)
        # calculating ball position
        self.ballAngle = self.sensor.getHeadAngle()[0]
        # writing into log file
        self.logger.info("Ball is at: "+str(self.ballAngle))
        # stop head tracking
        self.sensor.stopHeadTracker()
        
        #Using the correct behavior for the actual ball position
        if(self.ballAngle >= 0.2):
            self.motion.grabBall(0)
        elif(self.ballAngle <= -0.2):
            self.motion.grabBall(2)
        else:
            self.motion.grabBall(1)
        
        self.motion.closeRightHand()
        
        time.sleep(1)
        
        # getting up after picking the ball
        self.motion.getUp()
        
        time.sleep(1)
        
        # checking if ball was picked up
        if(self.sensor.isBallInHand()):
            # if ball is in hand, try to find the goal
            self.findGoal()
        else:
            # else, call ballWasLost
            self.ballWasLost()
        
    def findGoal(self):
    ###
    # Summary: Method for finding the goal
    # Parameters: self
    # Return: 
    ###   
    
        if (self.isStop):
            # end and return 1 if Nao is stopped
            self.end()
            return 1
                
        self.speech.say("Looking for the goal")
        self.motion.standUp()
        
        # set on the bottom camera. 0top 1bottom 
        self.sensor.setCamera(1) 
        self.sensor.subscribeToLandmarks()
        # pitch head
        self.motion.pitchHead(-30, 0.5)
        
        #Looking for the goal straight ahead
        time.sleep(self.retardSecond) 
        if(self.sensor.getLandmarkDistance()<10):
            self.sensor.unSubscribeFromLandMarks()
            # Nao found the goal
            self.goalFound()
            return 1
            
        self.speech.say("Could not find the goal")
        self.sensor.unSubscribeFromLandMarks()
        
        #Rotation around the ball with a newly calculated distance
        if(self.rotations != 11):
            # moving head
            self.motion.turnHead(0, 0.1)
            self.motion.pitchHead(15, 0.4)
            
            # starting tracking
            self.sensor.startHeadTracker()
            time.sleep(1)
            
            # calculate the position of the ball
            x = self.sensor.getBallPosition()[0]
            y = self.sensor.getBallPosition()[1]
            ballDistance = math.sqrt(math.pow(x,2)+math.pow(y,2))
            
            # write into log file the position of the ball
            self.logger.info("Ball distance: " + str(ballDistance))
            
            
            self.sensor.stopHeadTracker()
            
            # Nao rotates around the ball
            self.motion.rotateAroundBall(ballDistance, 30)
            self.rotations = self.rotations + 1
            # Nao tries to find the goal again
            self.findGoal()
        else:
            self.end()
        
    def goalFound(self):
    ###
    # Summary: Method which is called when the goal was found
    # Parameters: self
    # Return: if goal was found or not
    ###      
        
        if (self.isStop):
            self.end()
            return 1
                
        self.speech.say("Found the goal!")
        self.motion.standUp()
        
        # set on the bottom camera. 0top 1bottom 
        self.sensor.setCamera(1)
        self.sensor.subscribeToLandmarks()
        # moving head
        self.motion.pitchHead(-30, 0.5)
        
        
        self.sensor.subscribeToLandmarks()
        
        time.sleep(self.retardSecond*2)
        
        # locating landmark
        self.sensor.getLandmarkPosition()
        # getting landmark angle
        landMarkAngle = self.sensor.getLandmarkAngle()
        # writing info about where landmark is 
        self.logger.info("Landmark at: "+str(self.sensor.getLandmarkPosition()))
        
        if(landMarkAngle!=10):
            # Nao rotates around the ball according to distance to target and landmark angle 
            self.motion.rotateAroundBall(self.distanceToTarget, math.degrees(landMarkAngle))
            
            # moving head
            self.motion.turnHead(0, 0.1)
            self.motion.pitchHead(15, 0.4)
            
            # Nao says Aiming
            self.speech.say("Aiming!")
            
            # Nao starts head tracking
            self.sensor.startHeadTracker()
            time.sleep(1)
            
            # get info about position of the ball
            x = self.sensor.getBallPosition()[0]
            y = self.sensor.getBallPosition()[1]
            
            # stopping head tracking
            self.sensor.stopHeadTracker()
            
            # Nao moves to that position
            self.motion.moveTo(x-0.151,y-0.05, 0)
            # Nao kicks the ball
            self.motion.kickBall()
        
            self.sensor.unSubscribeFromLandMarks()
            self.end()
        else:
            # Nao speaks
            self.speech.say("Where did the goal go?")
            self.sensor.unSubscribeFromLandMarks()
            # Nao looks for the goal
            self.findGoal()
        
    def tooClose(self, colLeft, colRight):
    ###
    # Summary: this method control robot in case of collisions
    # Parameters: self, colLeft and colRight controls collisions from left and right sides
    # Return: --
    ###   
    
        if (self.isStop):
            self.end()
            return 1
        
        if(colLeft and colRight):
            # if sensors detect collisions on right and left sides that means there is an obstacle
            self.speech.say("Warning, obstacle ahead!")
            # stop moving
            self.motion.stopEverything()
            # stop head tracking
            self.sensor.stopHeadTracker()
            self.end()
        else:
            if(colLeft):
                # if left sensor detects collisions that means there is an obstacle on the left side
                self.logger.info("Colliding left")
                self.motion.stopEverything()
                self.sensor.stopHeadTracker()
                self.motion.moveTo(0, -0.2, 0)
                self.lookForBallCloseRange()
            if(colRight):
                # if right sensor detects collisions that means there is an obstacle on the right side
                self.logger.info("Colliding right")
                self.motion.stopEverything()
                self.sensor.stopHeadTracker()
                self.motion.moveTo(0, 0.2, 0)
                self.lookForBallCloseRange()
               

    def end(self):
    ###
    # Summary: method invokated in case of finishing 
    # Parameters: self
    # Return: --
    ###   
        # Nao stops every move
        self.motion.stopEverything()
        # Nao says Bye Bye
        self.speech.say("Bye Bye")
        # remove datas of the ball
        self.sensor.removeBallData()
        # Nao will be in resting position
        self.motion.rest()