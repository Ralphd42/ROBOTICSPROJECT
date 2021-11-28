from numpy.lib.function_base import append
import sim
import numpy as np
import csv
import math
import time
import cv2
import numpy as np
class Client:
    def __enter__(self):
         
        self.executedMovId1='notReady'
         
        sim.simxFinish(-1) # just in case, close all opened connections
        self.id=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        return self
    
    def __exit__(self,*err):
        sim.simxFinish(-1)
        print ('Program ended')

# load inverse kineiteics
def LoadInvKin(fileName):
    print("Starting LoadInvKin ")
    csv_file =  open(fileName,'r')  
    rdr = csv.reader(csv_file)#, delimiter=','
    print(list(rdr)[0])
    global inverseK
    for itm in  rdr:
        print("!")
        print (itm)
        print ("!")
        if( itm[0]  >= (dist -xThresh )   and  itm[0]  <= (dist +xThresh )):
            print (itm)
            print ("ADDED")
            inverseK.append(itm)
    inverseK = list(rdr)
    print("Ending LoadInvKin  ")
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
    print("Need to tweek invK")

def movAll( aAll):
    w=0
    while w<len(aAll):
        s = "j" + str(w+1)
        jnt =joints[s]
        sim.simxSetJointPosition(client.id,jnt["handle"],aAll[w]*math.pi/180,sim.simx_opmode_blocking)
        w+=1

def get1ImageforOrt():
    ec, res, img = sim.simxGetVisionSensorImage(client.id, hV1, 0, sim.simx_opmode_buffer )            
    while  ec != sim.simx_return_ok:           
        time.sleep(0.4)
        ec, res, img = sim.simxGetVisionSensorImage(client.id, hV1, 0, sim.simx_opmode_buffer )
    im = np.array(img, dtype =np.uint8)
    im.resize([res [0], res[1], 3])
    global imgdata
    imgdata = im.copy()

def OpenGrip():
    sim.simxSetJointPosition(client.id,griph  ,2 ,sim.simx_opmode_blocking)
    sim.simxSetJointPosition(client.id,griphmh,2 ,sim.simx_opmode_blocking)

def CloseGrip():
    sim.simxSetJointPosition(client.id,griph  ,.1,sim.simx_opmode_blocking)
    sim.simxSetJointPosition(client.id,griphmh,.1,sim.simx_opmode_blocking)

def getObjectstoPick():
    imghsv =cv2.cvtColor(imgdata,cv2.COLOR_BGR2HSV)
    #use threshholds from blob2.py
    # these can change
    # create a mask
    thMask =  cv2.inRange(imghsv, (56,179,120),(195,255,255))
    thMask = cv2.erode(thMask, None, iterations=3)
    thMask = cv2.dilate(thMask, None, iterations=3)
    prms = cv2.SimpleBlobDetector_Params()
    prms.minThreshold = 0 
    prms.maxThreshold = 100 
 
    # Filter by Area.
    prms.filterByArea = True
    prms.minArea = 400
    prms.maxArea = 20000
 
    # Filter by Circularity
    prms.filterByCircularity = False
    prms.minCircularity = 0.1
 
    # Filter by Convexity
    prms.filterByConvexity = False
    prms.minConvexity = 0.5
    # Filter by Inertia
    prms.filterByInertia = False
    prms.minInertiaRatio = 0.5
    # Detect blobs
    detector = cv2.SimpleBlobDetector_create(prms)
    keypoints = detector.detect(255-thMask)
    #detector = cv2.SimpleBlobDetector()
    #print(keypoints)
    global fruitLocs
    for kp in keypoints:
        y,z = kp.pt
        pnt =[]
        pnt [0] =dist
        pnt [1] = y
        pnt [2] = z  
        fruitLocs.append(pnt)

def pickItems():
    OpenGrip()
    for itm in fruitLocs:
        print("")
        movAll(findJointPost(itm))
        CloseGrip()
        movAll(basketcoords)
        OpenGrip()

with Client() as client:
    #start prog
    xThresh  =0.001
    dist     = 1
    inverseK =[]  #  inverse kinematics
    basketLoc=[]  # location of Basket
    imgdata  =[]   #this is the image retrieved from the sensor.
    fruitLocs=[] #  these are the locations of the fruits
    V1="V1"  #VisionSensor
    Yumi= 'YUMI'  #the YUMI
    rFinger = "gripper_r_finger_r_visual"  # end of the finger
    ec,hV1 =sim.simxGetObjectHandle(client.id,V1,sim.simx_opmode_blocking)
    LoadInvKin("invkWSALL.txt")
    print("____________________________________________________")
    #get joinds store in massive dict
    ec,rFingerh =sim.simxGetObjectHandle(client.id,rFinger,sim.simx_opmode_blocking)
    ec,Yumih = sim.simxGetObjectHandle(client.id,Yumi,sim.simx_opmode_blocking)
    #Gripper Joints
    grip  = "gripper_r_joint"
    ec,griph = sim.simxGetObjectHandle(client.id,grip,sim.simx_opmode_blocking)
    gripm = "gripper_r_joint_m"
    ec,griphmh = sim.simxGetObjectHandle(client.id,gripm,sim.simx_opmode_blocking)
    basketcoords=[]
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
    #start processing
    #1 get image ffrom vision sensor
    get1ImageforOrt()
    #process this data
    getObjectstoPick()
    #run the processor
    pickItems()