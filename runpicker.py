import sim
import numpy as np
import csv
class Client:
    
    def __enter__(self):
        self.fname ='ThreeDPlotData' #change to something better later this will hold xyz data
        self.executedMovId1='notReady'
        self.fname="invk.txt"
         
        sim.simxFinish(-1) # just in case, close all opened connections
        self.id=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        return self
    
    def __exit__(self,*err):
        sim.simxFinish(-1)
        print ('Program ended')





# load inverse kineiteics
def LoadInvKin(fileName):
    csv_file =  open(fileName)  
    rdr = csv.reader(csv_file, delimiter=',')
    print(rdr)
    global inverseK
    inverseK = list(rdr)
    print (inverseK)
    #line_count = 0
    #for row in csv_reader:
    #    line_count +=1

def findJointPost( coord):
    varrng = .0005
    for i in inverseK:
        print (i)
        if(i[0]>= (coord[0]-varrng)  and
            i[0]<= (coord[0]+varrng)  and
            i[1]>= (coord[1]-varrng)  and
            i[1]<= (coord[1]+varrng)  and
            i[2]>= (coord[2]-varrng)  and
            i[2]<= (coord[2]+varrng) ):
            print("found it")
            return i[3:]

def movAll( aAll):
        w=0
        while w<len(aAll):
            s = "j" + str(w+1)
            jnt =joints[s]
            sim.simxSetJointPosition(client.id,jnt["handle"],aAll[w]*math.pi/180,sim.simx_opmode_blocking)
            w+=1







with Client() as client:
    #start prog
    
    inverseK =[]  #  inverse kinematics
    basketLoc=[]
    LoadInvKin("invk.txt")
    Yumi= 'YUMI'
    rFinger = "gripper_r_finger_r_visual"
    #get joinds store in massive dict
    ec,rFingerh =sim.simxGetObjectHandle(client.id,rFinger,sim.simx_opmode_blocking)
    ec,Yumih = sim.simxGetObjectHandle(client.id,Yumi,sim.simx_opmode_blocking)
    joints ={}
    joints ["j1"] ={"name":"yumi_joint_1_r", "handle":0, "min":-169,"max":169}
    joints ["j2"] ={"name":"yumi_joint_2_r", "handle":0, "min":-144,"max": 44}
    joints ["j3"] ={"name":"yumi_joint_3_r", "handle":0, "min":-124,"max": 80}
    joints ["j4"] ={"name":"yumi_joint_4_r", "handle":0, "min":-290,"max":290}
    joints ["j5"] ={"name":"yumi_joint_5_r", "handle":0, "min":-88 ,"max":138}
    joints ["j6"] ={"name":"yumi_joint_6_r", "handle":0, "min":-229,"max":229}
    joints ["j7"] ={"name":"yumi_joint_7_r", "handle":0, "min":-169,"max":169}
    i=1
    while i<8:
        s = "j" + str(i) 
        ec,h   = sim.simxGetObjectHandle(client.id,joints[s]["name"],sim.simx_opmode_blocking)
        if ec!=0:
            print("Failed getting handles",ec ,s,joints[s]["name"])
        joints[s]["handle"] = h
        i+=1 






