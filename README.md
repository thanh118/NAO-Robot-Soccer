## Project: Build a Robot Soccer Apllication


Overview
---
NAO is a 58 cm tall programmable humanoid robot with 25 degrees of freedom, i.e. 25 different motors that control the joints of the robot. NAO robot weights 4.3 kg and has a built-in Linux-based operating system (NAOqi OS). Latest version of
NAO robots have a CPU Intel Atom 1.6 GHz, which introduces the challenge for programmers to develop the algorithms which would have lowest computational cost possible, so that even CPU of 1.6 GHz can handle the processing tasks. Each NAO robot has two cameras with maximum resolution of 1280x720, two infrared emitters and receivers, nine tactile sensors, sonar rangefinder, eight pressure sen-sors and four microphones. Development process of NAO robots began in 2004. Since then they have been widely used for research and educational purposes in universities and research centers all over the world. 

In this project, you will use Image processing and inverse kinematic to make robot play soccer. You will use the NAO API and NAO qi to detect the center of the ball and estimate distance from the ball to the robot. 

The project was written in Python. Use Nao behaviour include:
* ALProxy::ALMotion
* ALProxy::ALTextToSpeech
* ALProxy::ALBehaviorManager
* ALProxy::ALRedBallTracker
* ALProxy::ALRedBallDetection
* ALProxy::ALMemory

Structure of code:
* 1/ NAO_config.py: Set IP and PORT for the Robot, and test the connection of all Proxy on Nao, if there are some part not work --> return error!
* 2/ NAO_controller.py: The set of main function to make NAO play soccer.
* 3/ NAO_logger.py: Return log file for NAO robot.
* 4/ NAO_motion.py: The set of functions to control NAO motion like stand up, run fast, kick ball...
* 5/ NAO_sensor.py: The set of functions control NAO sensors(Ultrasound sensor, tactic_head sensor..)
* 6/ NAO_main.py: main functions.
* 7/ UI.py: Frontend for the app NAO_play soccer. Still developing.

In general, this project is make NAO robot looking, define red ball position in any positon in the room, aim it!, walking to it, then found the goal position by walking around, then shoot the ball the goal. The all project was written in Python, if user want to use the code, just download code, change the IP and PORT of your robot, then run the NAO_main.py.

