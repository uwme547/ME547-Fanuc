import time
import socket
import math
class Fanuc:
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('127.0.0.1', 65432))
    serv.listen(5)
    conn, addr = serv.accept()
    speed = 20
    l1 = 260.0
    l2 = math.sqrt(290.0**2+20.0**2)
    l3 = 78.0

    def __init__(self):
        pass

    def __del__(self):
        self.conn.send(b"0 ")
        self.waitForResponse()
        time.sleep(2)
        self.conn.close()
        print('client disconnected')
    
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
        
    def moveJointsFanuc(self, th1, th2, th3, th4, th5):
        string = self.serialize([1,th1, th2, th3, th4, th5, self.speed])
        print("moveJoints goint to " + string)
        byte = bytes(string, 'utf-8')
        self.conn.send(byte)
        self.waitForResponse()
    
    def moveJoints(self, th1, th2, th3, th4, th5):
        th = self.DHtoFanuc([th1, th2, th3, th4, th5])
        self.moveJointsFanuc(th[0], th[1], th[2],th[3],th[4])

    def moveToPosition(self, x, y, z, alpha):
        th = self.invKin(x, y, z, alpha)
        self.moveJoints(th[0], th[1], th[2], th[3], th[4])
    
    def moveLin(self, x, y, z, w, p, r):
        string = self.serialize([4,x, y, z, w, p, r, self.speed])
        byte = bytes(string, 'utf-8')
        self.conn.send(byte)
        self.waitForResponse()


    def openGripper(self):
        self.conn.send(b"2 ")
        self.waitForResponse()

    def closeGripper(self):
        self.conn.send(b"3 ")
        self.waitForResponse()

    def serialize(self, args):
        string = ""
        for arg in args:
            string += str(arg) + " "
        return string
    
    def invKin(self, x, y, z, alpha):
        th1 = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)
        s = z + self.l3
        cos3 = (r**2 + s**2 - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        th3 = math.atan2(-math.sqrt(1 - cos3**2), cos3)
        th2 = -math.atan2(s, r) + math.atan2(self.l2 * math.sin(th3), self.l1 + self.l2 * math.cos(th3))
        th4 = th2 - th3
        th5 = alpha * math.pi / 180.0 - th1 - math.pi / 2

        DH = [th1, th2, th3, th4, th5]

        for th in range(0,len(DH)):
            DH[th] = DH[th] * 180.0 / math.pi

        return DH

    def DHtoFanuc(self, DH):
        fanucAngles = []
        fanucAngles.append(round(DH[0],6))
        fanucAngles.append(round(DH[1] + 90.0,6))
        fanucAngles.append(round(DH[2] - DH[1] - math.atan2(20.0, 290.0) * 180.0 / math.pi,6))
        fanucAngles.append(round(DH[3] - 90.0 + math.atan2(20.0, 290.0) * 180.0 / math.pi,6))
        fanucAngles.append(round(DH[4],6))

        return fanucAngles


    
    def waitForResponse(self):
        encoding = 'utf-8'
        data = self.conn.recv(10024)
        from_client = str(data,encoding)
        if (from_client != "done"):
            time.sleep(0.5)
            self.waitForResponse()
        else:
            print(from_client)
            return