import socket
import time


if __name__ == "__main__": 
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.connect(("127.0.0.1", 65432))
    encoding = 'utf-8'
    while(True):
        data = str(serv.recv(10024),encoding).split()
        
        if (data[0] == "0"):
            print("Shutting down")
            serv.send(b"done")
            break
        elif (data[0] == "1"):
            print("Using moveJoint to move to, th1: " + data[1] + " th2: " + data[2] + " th3: " +  data[3] + " th4: " + data[4] +  " th5: " + data[5] + " with speed:" + data[6] + "\n")
            serv.send(b"done")
        elif (data[0] == "2"):
            print("Openning gripper \n")
            serv.send(b"done")
        elif (data[0] == "3"):
            print("Closing gripper \n")
            serv.send(b"done")
        elif (data[0] == "4"):
            print("Using moveLin to move to, x: " + data[1] + " y: " + data[2] + " z: " +  data[3] + " w: " + data[4] + " p: " + data[5] +  " r: " + data[6] + " with speed:" + data[6] + "\n")
            serv.send(b"done")
    serv.close()            