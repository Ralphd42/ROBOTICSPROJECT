# Make sure to have CoppeliaSim running, with followig scene loaded:
#
# .ttt
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
from posixpath import join
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
    sIntv =0.000000001#.0625
    def degToRad(deg  ):
        return deg* math.pi/180
    def radToDeg(rad):
        return rad*180/math.pi

    def TrackJointh(hndl):
        i=-180
        while i<180:
            
            sim.simxSetJointPosition(client.id,hndl,i*math.pi/180,sim.simx_opmode_blocking)
            c,pos = sim.simxGetJointPosition(client.id,hndl,sim.simx_opmode_blocking)
            lc =getArmPos()
            print (lc)
            print( "jp = ",i, c, radToDeg(   pos)   )
            i +=1
            #time.sleep(sIntv)
    def TrackJoint(jname):
        print (jname)
        jnt =joints[jname]
        print(jnt)
        i=jnt["min"]
        while i<=jnt["max"]:
            
            sim.simxSetJointPosition(client.id,jnt["handle"],i*math.pi/180,sim.simx_opmode_blocking)
            c,pos = sim.simxGetJointPosition(client.id,jnt["handle"],sim.simx_opmode_blocking)
            lc =getArmPos()
            print ("i {}|p {}|arm {} ".format(i,radToDeg(   pos),lc))
            #print( "jp = ",i, c, radToDeg(   pos)   )
            i +=1
            #time.sleep(sIntv)
              
    def getArmPos():
        st, loc =sim.simxGetObjectPosition(client.id,rFingerh, -1,  sim.simx_opmode_blocking)
        return loc

    def movAll( aAll):
        w=0
        while w<len(aAll):
            s = "j" + str(w+1)
            jnt =joints[s]
            sim.simxSetJointPosition(client.id,jnt["handle"],aAll[w]*math.pi/180,sim.simx_opmode_blocking)
            w+=1

    
    def invK():
        stp=1
        for a in range (joints["j1"]["min"],joints["j1"]["max"],stp):
            for b in range (joints["j2"]["min"],joints["j2"]["max"],stp):
                for c in range (joints["j3"]["min"],joints["j3"]["max"],stp):
                    for d in range (joints["j4"]["min"],joints["j4"]["max"],stp):
                        for e in range (joints["j5"]["min"],joints["j5"]["max"],stp):
                            for f in range (joints["j6"]["min"],joints["j6"]["max"],stp):
                                for g in range (joints["j7"]["min"],joints["j7"]["max"],stp):
                                    movAll([a,b,c,d,e,f,g])

    
    
    
    
    
    
    print("running")

    if client.id!=-1:
        print ('Connected to remote API server')
        Yumi= 'YUMI'
        rFinger = "gripper_r_finger_r_visual"
        #get joinds store in massive dict
        ec,rFingerh =sim.simxGetObjectHandle(client.id,rFinger,sim.simx_opmode_blocking)
        print( "ecf",ec)
        ec,Yumih = sim.simxGetObjectHandle(client.id,Yumi,sim.simx_opmode_blocking)
        print ("ecy",ec)
        joints ={}
        joints ["j1"] ={"name":"yumi_joint_1_r", "handle":0, "min":-169,"max":169}
        joints ["j2"] ={"name":"yumi_joint_2_r", "handle":0, "min":-144,"max": 44}
        joints ["j3"] ={"name":"yumi_joint_3_r", "handle":0, "min":-124,"max": 80  }
        joints ["j4"] ={"name":"yumi_joint_4_r", "handle":0, "min":-290  ,"max":290  }
        joints ["j5"] ={"name":"yumi_joint_5_r", "handle":0, "min":-88   ,"max":138  }
        joints ["j6"] ={"name":"yumi_joint_6_r", "handle":0, "min":-229  ,"max":229  }
        joints ["j7"] ={"name":"yumi_joint_7_r", "handle":0, "min":-169,"max":169}
        i=1
        while i<8:
            s = "j" + str(i) 
            ec,h   = sim.simxGetObjectHandle(client.id,joints[s]["name"],sim.simx_opmode_blocking)
            if ec!=0:
                print("Failed getting handles",ec ,s,joints[s]["name"])
            joints[s]["handle"] = h
            i+=1 

        
        






        

        
             
        
        #j1      = "yumi_joint_1_r"#"yumi_link_1_r_visible" 
        #j2      = "yumi_joint_2_r"
        #j3      = "yumi_joint_3_r"
        #j4      = "yumi_joint_4_r"
        #j5      = "yumi_joint_5_r"
        #j6      = "yumi_joint_6_r"

        
        
        
        #ec,j2h   = sim.simxGetObjectHandle(client.id,j2,sim.simx_opmode_blocking)
        #ec,j3h   = sim.simxGetObjectHandle(client.id,j3,sim.simx_opmode_blocking)
        #ec,j4h   = sim.simxGetObjectHandle(client.id,j4,sim.simx_opmode_blocking)
        #ec,j5h   = sim.simxGetObjectHandle(client.id,j5,sim.simx_opmode_blocking)
        #ec,j6h   = sim.simxGetObjectHandle(client.id,j6,sim.simx_opmode_blocking)
        #client.stringSignalName1=RobotArm+'_executedMovId'
        #f3dout = open(client.fname, "a")
        #st, loc =sim.simxGetObjectPosition(client.id,Yumih, -1,  sim.simx_opmode_blocking)
        #print(st )
        #print (loc) 
        
        #move to center
        err, pos = sim.simxGetObjectPosition(client.id,Yumih,-1,sim.simx_opmode_blocking)  
        sim.simxSetObjectPosition(client.id,Yumih,-1,[0,0,0],sim.simx_opmode_blocking)
        sim.simxSetObjectOrientation(client.id,Yumih,-1,[0,0,0],sim.simx_opmode_blocking)
        # lets get moving some joints
        
        sim.simxSetJointPosition(client.id,joints ["j3"]["handle"],0,sim.simx_opmode_blocking)
        #TrackJoint(joints["j5"]["handle"])
        #TrackJoint("j5")
        invK()
        
        
        
        #i=-180
        ##while i<180:
         #   
         #   sim.simxSetJointPosition(client.id,j1h,i*math.pi/180,sim.simx_opmode_blocking)
         #   c,pos = sim.simxGetJointPosition(client.id,j1h,sim.simx_opmode_blocking)
         #   print( "jp = ",i, c, radToDeg(   pos)   )
         #   i +=1
         #   time.sleep(sIntv)

        sim.simxStopSimulation(client.id,sim.simx_opmode_blocking)
        
        #sim.simxGetStringSignal(client.id,client.stringSignalName1,sim.simx_opmode_discontinue)
       
        sim.simxGetPingTime(client.id)

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(client.id)
    else:
        print ('Failed connecting to remote API server')
        print('Did you try simRemoteApi.start(19999)')
