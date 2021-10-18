# Make sure to have CoppeliaSim running, with followig scene loaded:
#
# scenes/messaging/RDmovementViaRemoteApi.ttt
# If fail to connect try the following 
# simRemoteApi.start(19999)
# Do not launch simulation, then run this script
#
# The client side (i.e. this script) depends on:
#
# sim.py, simConst.py, and the remote API library available
# in programming/remoteApiBindings/lib/lib
# Additionally you will need the python math and msgpack modules

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

import math
import msgpack
import time
class Client:
    def __enter__(self):
        self.fname ='ThreeDPlotData' #change to something better later this will hold xyz data
        self.executedMovId1='notReady'
         
        sim.simxFinish(-1) # just in case, close all opened connections
        self.id=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        return self
    
    def __exit__(self,*err):
        sim.simxFinish(-1)
        print ('Program ended')

with Client() as client:
    #constants
    sIntv =.0625
    def degToRad(deg  ):
        return deg* math.pi/180
    def radToDeg(rad):
        return rad*180/math.pi

    def TrackJoint(hndl):
        i=-180
        while i<180:
            
            sim.simxSetJointPosition(client.id,hndl,i*math.pi/180,sim.simx_opmode_blocking)
            c,pos = sim.simxGetJointPosition(client.id,hndl,sim.simx_opmode_blocking)
            print( "jp = ",i, c, radToDeg(   pos)   )
            i +=1
            time.sleep(sIntv)  





    print("running")

    if client.id!=-1:
        
        print ('Connected to remote API server')

        Yumi= 'YUMI'
        client.id    
        rFinger = "rFinger" 
        j1      = "yumi_joint_2_r"
        j3      = "yumi_joint_3_r"
        ec,rFingerh =sim.simxGetObjectHandle(client.id,rFinger,sim.simx_opmode_blocking)
        ec,Yumih = sim.simxGetObjectHandle(client.id,Yumi,sim.simx_opmode_blocking)
        ec,j1h   = sim.simxGetObjectHandle(client.id,j1,sim.simx_opmode_blocking)
        ec,j3h   = sim.simxGetObjectHandle(client.id,j3,sim.simx_opmode_blocking)
        #client.stringSignalName1=RobotArm+'_executedMovId'
        #f3dout = open(client.fname, "a")
        st, loc =sim.simxGetObjectPosition(client.id,Yumih, -1,  sim.simx_opmode_blocking)
        print(st )
        print (loc) 
        #move to center
        err, pos = sim.simxGetObjectPosition(client.id,Yumih,-1,sim.simx_opmode_blocking)  
        sim.simxSetObjectPosition(client.id,Yumih,-1,[0,0,0],sim.simx_opmode_blocking)
        sim.simxSetObjectOrientation(client.id,Yumih,-1,[0,0,0],sim.simx_opmode_blocking)
        # lets get moving some joints
        TrackJoint(j3h)
        
        
        
        
        
        i=-180
        while i<180:
            
            sim.simxSetJointPosition(client.id,j1h,i*math.pi/180,sim.simx_opmode_blocking)
            c,pos = sim.simxGetJointPosition(client.id,j1h,sim.simx_opmode_blocking)
            print( "jp = ",i, c, radToDeg(   pos)   )
            i +=1
            time.sleep(sIntv)

        sim.simxStopSimulation(client.id,sim.simx_opmode_blocking)
        
        #sim.simxGetStringSignal(client.id,client.stringSignalName1,sim.simx_opmode_discontinue)
       
        sim.simxGetPingTime(client.id)

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(client.id)
    else:
        print ('Failed connecting to remote API server')
        print('Did you try simRemoteApi.start(19999)')
