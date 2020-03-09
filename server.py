from lib.fanuc import Fanuc
import time
if __name__ == "__main__":
    robot = Fanuc() 
    robot.setSpeed(20)
    robot.moveToPosition(400, -100, -100, 0)
    robot.setSpeed(50)
    robot.moveJoints(10,0,0,0,0)
    robot.moveLin(435,-100,-120,-180,0,90)
    time.sleep(5)
  
