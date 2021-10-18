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
    print("running")

    if client.id!=-1:

        print ('Connected to remote API server')

        RobotArm= 'blueArm'
        client.id    
        EndofArm = "blueArm_connection" 
        ec,EndofArmh =sim.simxGetObjectHandle(client.id,EndofArm,sim.simx_opmode_blocking)
        ec,RobotArmh = sim.simxGetObjectHandle(client.id,RobotArm,sim.simx_opmode_blocking)
        client.stringSignalName1=RobotArm+'_executedMovId'
        f3dout = open(client.fname, "a")
        
        def waitForMovementExecuted1(id):
            while client.executedMovId1!=id:
                retCode,s=sim.simxGetStringSignal(client.id,client.stringSignalName1,sim.simx_opmode_buffer)
                if retCode==sim.simx_return_ok:
                    if type(s)==bytearray:
                        s=s.decode('ascii') # python2/python3 differences
                    client.executedMovId1=s


        def move( Tconfig, seqName):
            # Set-up some movement variables:
            mVel=40*math.pi/180
            mAccel=60*math.pi/180
            maxVel=[mVel,mVel,mVel,mVel,mVel,mVel]
            maxAccel=[mAccel,mAccel,mAccel,mAccel,mAccel,mAccel]
            targetVel=[0,0,0,0,0,0]
            
            for i in range(len(Tconfig)):
                Tconfig[i] = Tconfig[i] * math.pi/180
            
            movementData={"id":seqName,"type":"mov","targetConfig":Tconfig,"targetVel":targetVel,"maxVel":maxVel,"maxAccel":maxAccel}
            packedMovementData=msgpack.packb(movementData)
            rv =sim.simxCallScriptFunction(client.id,RobotArm,sim.sim_scripttype_childscript,'legacyRapiMovementDataFunction',[],[],[],packedMovementData,sim.simx_opmode_oneshot)
             
            if( rv[0]==8):
                print( "Failed legacyRapiMovementDataFunction")
            else:

            # Execute fourth movement sequence:
                rv =sim.simxCallScriptFunction(client.id,RobotArm,sim.sim_scripttype_childscript,'legacyRapiExecuteMovement',[],[],[],seqName,sim.simx_opmode_oneshot)
             
                if( rv[0]==8):
                    print( "Failed legacyRapiExecuteMovement")
                else:
                    # Wait until above movement sequence finished executing:
                    waitForMovementExecuted1(seqName)
                    WriteArmLoc(Tconfig)
        
        def WriteArmLoc(Tconfig  ):
            st, loc =sim.simxGetObjectPosition(client.id,EndofArmh, -1,  sim.simx_opmode_blocking)
            #print (loc )
            if (st==0):
                txtOutLn = txt3 = "{},{},{},{},{},{}\n".format(Tconfig[1],Tconfig[2],Tconfig[4],loc[0],loc[1],loc[2]) 


                f3dout.write(txtOutLn)
            if(st!=0):
                print("Can't locate Arm")


        # Start streaming client.stringSignalName1 and client.stringSignalName2 string signals:
        sim.simxGetStringSignal(client.id,client.stringSignalName1,sim.simx_opmode_streaming)
         

        
        # Start simulation:
        sim.simxStartSimulation(client.id,sim.simx_opmode_blocking)

        # Wait until ready:
        waitForMovementExecuted1('ready') 


        #move([0,-170*math.pi/180,-170*math.pi/180,0,-170*math.pi/180,0],'seq5')
        #move([0,-90*math.pi/180,-90*math.pi/180,0,-90*math.pi/180,0],'seq6')

        stp =10
        jbRng = [0,-109,-15,0,-20,0]
        
        jtRng = [0,109, 45,0, 45,0]

        #jbRng = [0,-109,-114,0,-114,0]
        #jtRng = [0, 109, 114,0, 114,0]


         
        sIntv =.5
        for x in range (jbRng[1],jtRng[1],stp):
            for y in range (jbRng[2], jtRng[2],stp):
                for z in range (jbRng[4], jtRng[4],stp):
                     
                    print('B - '  +str(x) +'  ' + str(y)   + ' ' +str(z)  ) 
                    move([0,  x , y ,0, z ,0],'seq' +str(x))
                    #col2 =sim.simxCheckCollision(client.id,EndofArmh,-2,sim.simx_opmode_blocking)
                     
                    #print (col2)
                    #col3  =sim.simxCheckCollision(client.id,RobotArmh ,-2,sim.simx_opmode_blocking)
                    #print(col3)
                    # this doesn't seem to work
                    col3  =sim.simxCheckCollision(client.id,EndofArmh,RobotArmh ,sim.simx_opmode_blocking)
                    print(col3)
                    print( 'A - ' +str(x) +'  ' + str(y) + ' ' +str(z)  ) 
                    time.sleep(sIntv)
        f3dout.close()

        sim.simxStopSimulation(client.id,sim.simx_opmode_blocking)
        sim.simxGetStringSignal(client.id,client.stringSignalName1,sim.simx_opmode_discontinue)
       
        sim.simxGetPingTime(client.id)

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(client.id)
    else:
        print ('Failed connecting to remote API server')
        print('Did you try simRemoteApi.start(19999)')
