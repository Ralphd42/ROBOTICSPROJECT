try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('simRemoteApi.start(19999)')
#import sim
import math
from posixpath import join
import msgpack
import time
import cv2
import numpy as np
from PIL import Image as I
def degToRad(deg  ):
    return deg* math.pi/180
    
def radToDeg(rad):
    return rad*180/math.pi
class Client:
    def __enter__(self):
        
        #self.executedMovId1='notReady'
        self.fname="invBasket.txt"
         
        sim.simxFinish(-1) # just in case, close all opened connections
        self.id=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        return self
    
    def __exit__(self,*err):
        sim.simxFinish(-1)
        print ('Program ended')
with Client() as client:    
    def get1ImageforOrt( x,y,z):
        sim.simxSetObjectOrientation(client.id,hV1,rFloor,[degToRad(x),degToRad(y),degToRad(z)],sim.simx_opmode_blocking)
        ec, res, img = sim.simxGetVisionSensorImage(client.id, hV1, 0, sim.simx_opmode_buffer )            
        while  ec != sim.simx_return_ok:           
            time.sleep(0.4)
            ec, res, img = sim.simxGetVisionSensorImage(client.id, hV1, 0, sim.simx_opmode_buffer )
        im = np.array(img, dtype =np.uint8)
        im.resize([res [0], res[1], 3])
        cv2.imshow("Result view", im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    
    V1="V1"
    floor ="Floor_visible"
    ec,hV1 =sim.simxGetObjectHandle(client.id,V1,sim.simx_opmode_blocking)
    print( "hV1",ec,hV1)
    ec,res,img = sim.simxGetVisionSensorImage(client.id, hV1, 0, sim.simx_opmode_streaming)
    ec,rFloor   = sim.simxGetObjectHandle(client.id,floor  ,sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(client.id,rFloor,-1,[0,0,0],sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(client.id,hV1,rFloor,[0,.1,.8],sim.simx_opmode_blocking)
    st, pRV1 =sim.simxGetObjectPosition(client.id,hV1, -1,  sim.simx_opmode_blocking)
    print ("pv1", pRV1)
    get1ImageforOrt( 0,140,0)

def loopForImage():
    for x in range (0,360,40):
        for y in range(0,360,40):
            for z in range(0,360,40):
                sim.simxSetObjectOrientation(client.id,hV1,rFloor,[degToRad(x),degToRad(y),degToRad(z)],sim.simx_opmode_blocking)
                time.sleep(0.4)
                ec, res, img = sim.simxGetVisionSensorImage(client.id, hV1, 0, sim.simx_opmode_buffer )            
                if ec == sim.simx_return_ok:
                    print(x,y,z)
                    for xx in img:
                        if xx!=0:
                            im = np.array(img, dtype =np.uint8)
                            im.resize([res [0], res[1], 3])
                            #cv2.imshow(im,origin = 'lower')
                            cv2.imshow("Result view", im)
                            cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            #quit()
                            break
                else:
                    print ("Failed")
                    quit()