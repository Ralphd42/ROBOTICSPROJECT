# the purpose of this is to help set up initial layout of Page.
# it make sure simulation has stated at 0




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
class Client:
    def __enter__(self):
        
        #self.executedMovId1='notReady'
        self.fname="invkWS.txt"
         
        sim.simxFinish(-1) # just in case, close all opened connections
        self.id=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        return self
    
    def __exit__(self,*err):
        sim.simxFinish(-1)
        print ('Program ended')

with Client() as client:
    #sim.simxStartSimulation(client.id,sim.simx_opmode_blocking)
    Yumi= 'YUMI'
    rFinger = "gripper_r_finger_r_visual"
    floor ="Floor_visible"
    basket = "Basket_visible"
    tree = "indoorPlant_visible"
    apple = "RedApple1"

    ec,Yumih    = sim.simxGetObjectHandle(client.id,Yumi   ,sim.simx_opmode_blocking)
    ec,rFingerh = sim.simxGetObjectHandle(client.id,rFinger,sim.simx_opmode_blocking)
    ec,rFloor   = sim.simxGetObjectHandle(client.id,floor  ,sim.simx_opmode_blocking)
    ec,rBasket  = sim.simxGetObjectHandle(client.id,basket ,sim.simx_opmode_blocking)
    ec,rtree    = sim.simxGetObjectHandle(client.id,tree   ,sim.simx_opmode_blocking)
    ec,rApple   = sim.simxGetObjectHandle(client.id,apple  ,sim.simx_opmode_blocking)

    rbase = -1
    #rbase = rFloor


    def degToRad(deg  ):
        return deg* math.pi/180
    
    def radToDeg(rad):
        return rad*180/math.pi

    def getArmPos():
        st, loc =sim.simxGetObjectPosition(client.id,rFingerh, -1,  sim.simx_opmode_blocking)
        return loc

    def getArmOrientation():
        #st, loc =sim.simxGetObjectPosition(client.id,rFingerh, -1,  sim.simx_opmode_blocking)
        st, orr=sim.simxGetObjectOrientation(client.id,rFingerh,-1,sim.simx_opmode_blocking)
        return orr

    err, pos = sim.simxGetObjectPosition(client.id,Yumih,-1,sim.simx_opmode_blocking)  
    #position YUMI
    sim.simxSetObjectPosition(client.id,rFloor,-1,[0,0,0],sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(client.id,Yumih,rFloor,[0,0,0],sim.simx_opmode_blocking)
    sim.simxSetObjectOrientation(client.id,Yumih,rFloor,[0,0,0],sim.simx_opmode_blocking)
    
    #basket
    sim.simxSetObjectOrientation(client.id,rBasket,rFloor,[0,0,0],sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(client.id,rBasket,rFloor,[0,-.5,.05],sim.simx_opmode_blocking)
    st, basketPos =sim.simxGetObjectPosition(client.id,rBasket, rFloor,  sim.simx_opmode_blocking)
    print(basketPos)
    
    #tree
    st, treePos =sim.simxGetObjectPosition(client.id,rtree, rFloor,  sim.simx_opmode_blocking)
    sim.simxSetObjectPosition(client.id,rtree,rFloor,[.5 , 0 ,.26],sim.simx_opmode_blocking)
    st, treePos =sim.simxGetObjectPosition(client.id,rtree, rFloor,  sim.simx_opmode_blocking)
    print("tr",treePos)

    #APPLE
    st, applepos =sim.simxGetObjectPosition(client.id,rApple, rFloor,  sim.simx_opmode_blocking)
    #sim.simxSetObjectPosition(client.id,rApple,rFloor,[.5,0,.4],sim.simx_opmode_blocking)
    
    print ("APPLE" ,applepos)







