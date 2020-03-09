from lib.fanuc import Fanuc
import time
if __name__ == "__main__":
    robot = Fanuc() 
    robot.setSpeed(20)
    robot.moveToPosition(400, -100, -100, 0)
    time.sleep(5)
  
