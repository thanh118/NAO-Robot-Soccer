###
# Summary: this class will handle all the log message in case of error, info or any
#          other information we need
# Parameters: none
# Return: none
###
from time import localtime, strftime
from cgi import logfile
import os


class Logger:
    logLevel = 1
    logToFile = True
    # it creates a new file in which we will write the messages
    logFile = open("logfile.log", "w")

    def __init__(self):
        ###
        # Summary: initialize logger class
        # Parameters: self
        # Return: --
        ###
        self.info("Logger-Class initialized")
        # self.clearLogFile()

    def info(self, infoMessage):
        ###
        # Summary: this method gives us general information
        # Parameters: self, infoMessage will be the message we want to write in the log file
        # Return: --
        ###
        self.writeToLog("[Info] " + self.getTime() + ": " + infoMessage)
        print "[Info] " + self.getTime() + ": " + infoMessage

    def warn(self, warnMessage):
        ###
        # Summary: This method gives us a warning message so we know something is not
        #         going well
        # Parameters: self, warnMessage will be the message written into log file
        # Return: --
        ###
        self.writeToLog("[Warning] " + self.getTime() + ": " + warnMessage)
        print "[Warning] " + self.getTime() + ": " + warnMessage

    def fatal(self, fatalMessage):
        ###
        # Summary: method called in case of fatal error
        # Parameters: self, fatalMessage will be the message written into log file
        # Return: --
        ###
        self.writeToLog("[FATAL] " + self.getTime() + ": " + fatalMessage)
        self.writeToLog("[FATAL] " + self.getTime() + ": SYSTEM WILL NOW EXIT!")
        print "[FATAL] " + self.getTime() + ": " + fatalMessage
        print "[FATAL] " + self.getTime() + ": SYSTEM WILL NOW EXIT!"
        exit(1)

    def getTime(self):
        ###
        # Summary: method to know the local time
        # Parameters: self
        # Return: the local time in the following format (h:m:s)
        ###
        return strftime("%H:%M:%S", localtime())

    def setLogLevel(self, level):
        ###
        # Summary: method to set the level of the errors
        # Parameters: self, level of the error
        # Return: --
        ###
        if (level == 1):
            self.logLevel = 1
        elif (level == 2):
            self.logLevel = 2
        elif (level == 3):
            self.logLevel = 3
        else:
            self.warn("Log level value error.")

    def setLogToFile(self, boolean):
        ###
        # Summary: this method confirm we can write log messages into a file
        # Parameters: self, boolean will set the value of variable logToFile
        # Return: --
        ###
        self.logToFile = boolean

    def writeToLog(self, message):
        ###
        # Summary: this method will write the log message into a file
        # Parameters: sefl, message will be written into the log file
        # Return: --
        ###
        self.logFile.write(message + "\n")

    def clearLogFile(self):
        ###
        # Summary: this method will remove the log file
        # Parameters: self
        # Return:
        ###
        os.remove("logfile.log")