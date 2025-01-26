import binascii
import mmap
from pickle import FALSE
import numpy as np
from DataInterfacePython import *
import math
from xml.dom.minidom import parseString
from V2X.Message import *
from V2X import Build_BSM
from V2X import Build_RSI
from V2X import Build_RSM
from V2X import Build_SPAT
from V2X import Build_SSM
from V2X import Build_PMM
from V2X import Build_VIR
from V2X import Build_RSC
from V2X import Build_PSM
from V2X import Build_RTCM
import asn1tools
import os
from socket import *
#获取文件父目录
Agent_V2X_Dir = os.path.dirname(__file__)
 
ltevCoder = None
ltevCoder_2 = None


# 仿真实验启动时回调
def ModelStart(userData):
    # 构造主车控制总线读取器
    userData['ego_control'] = BusAccessor(userData['busId'], 'ego_control','time@i,valid@b,throttle@d,brake@d,steer@d,mode@i,gear@i')
    # 构造主车状态总线读取器1
    userData['ego_state'] = BusAccessor(userData['busId'], 'ego', 'time@i,x@d,y@d,z@d,yaw@d,pitch@d,roll@d,speed@d')
    # 构造主车状态总线读取器2
    userData['ego_extra'] = BusAccessor(userData['busId'], 'ego_extra','time@i,VX@d,VY@d,VZ@d,AVx@d,AVy@d,AVz@d,Ax@d,Ay@d,Az@d,AAx@d,AAy@d,AAz@d')
    # 告警信息总线读取器
    userData["warning"] = BusAccessor(userData['busId'], "warning", 'time@i,type@b,64@[,text@b')   
    # BSM总线读取器
    userData['V2X_BSM'] = BusAccessor(userData['busId'], 'V2X_BSM.0', 'time@i,100@[,id@i,delaytime@i,x@d,y@d,z@d,yaw@d,pitch@d,roll@d,speed@d')
    # RSM总线读取器
    userData['V2X_RSM'] = BusAccessor(userData['busId'], 'V2X_RSM.0', 'time@i,100@[,id@i,delaytime@i,type@b,shape@i,x@d,y@d,z@d,yaw@d,pitch@d,roll@d,speed@d')
    # RSI总线读取器
    userData['V2X_RSI'] = BusAccessor(userData['busId'], 'V2X_RSI.0', 'time@i,100@[,id@i,delaytime@i,shape@i,x@d,y@d,z@d,yaw@d,pitch@d,roll@d')
    # RSM总线读取器
    userData['V2X_MAP'] = BusAccessor(userData['busId'], 'V2X_MAP.0', 'time@i,100@[,id@i,delaytime@i')
    # RSI总线读取器
    userData['V2X_SPAT'] = BusAccessor(userData['busId'], 'V2X_SPAT.0', 'time@i,100@[,id@i,delaytime@i,x@d,y@d,z@d,yaw@d,pitch@d,roll@d')
    # 交通参与物信息读取，type==1为行人,type==0为车辆
    userData['traffic'] = DoubleBusReader(userData['busId'],'traffic','time@i,100@[,id@i,type@b,shape@i,x@f,y@f,z@f,yaw@f,pitch@f,roll@f,speed@f') 
    # GNSS总线读取器
    userData['GNSS'] = BusAccessor(userData['busId'],'GNSS.0','Timestamp@i,Longitude@d,Latitude@d,Altitude@d,Heading@d,Velocity@d')  
    # userData['UTM'] = getUtmOrigin()  #(zone, x, y, z)
    userData['ego_traffic'] = BusAccessor(userData['busId'],'ego_traffic','time@i,lane@i,station@d,lateral@d,internal@b,nextJunction@i') 
    #车灯状态
    userData["global9"] = BusAccessor(userData['busId'], 'global.9', 'time@i,variable@d')

    userData['mm'] = mmap.mmap(fileno=-1, length=4 + 360 * 16, tagname="panosim.0.FreespacePerceptor.0")
        
    # 初始化变量，推荐使用此方法定义对于Agent的全局变量
    userData['last'] = 0
    userData['Vx'] = []
    userData['Time'] = []
    userData['i_term_last'] = 0
    userData['v_error_last'] = 0
    userData['steer'] = []
    userData['sl_ego'] = 0
    userData['pedestrians_points'] = {}

    
    #初始化asn打包器
    asnPath=Agent_V2X_Dir+'\\V2X\\asn\\LTEV.asn'
    paths = []
    whole_paths = []
    for filename in os.listdir(Agent_V2X_Dir+'\\V2X\\asn\\day2'):
        paths.append(filename)
    for path in paths:
        whole_paths.append(Agent_V2X_Dir+'\\V2X\\asn\\day2\\' + path)
    global ltevCoder ,ltevCoder_2
    # ltevCoder=asn1tools.compile_files(asnPath, 'ber', numeric_enums=True) 
    ltevCoder=asn1tools.compile_files(asnPath, 'uper', numeric_enums=True) 
    ltevCoder_2=asn1tools.compile_files(whole_paths, 'uper', numeric_enums=True) 
    
    print("-----This is the initialization of Agent_V2X-----")
    

# 每个仿真周期(10ms)回调
def ModelOutput(userData):
    basell = [39.5427,116.2317] #PanoSim原点对应的经纬度值
    # 读主车车辆状态
    ego_time, ego_x, ego_y, ego_z, ego_yaw, ego_pitch, ego_roll, ego_speed = userData['ego_state'].readHeader()
    _, valid_last, throttle_last, brake_last, steer_last, mode_last, gear_last = userData['ego_control'].readHeader()
    _, VX, VY, VZ, AVx, AVy, AVz, Ax, Ay, Az, AAx, AAy, AAz = userData['ego_extra'].readHeader()
        
    # 读取BSM(即出主车外的其他交通车)信息
    bsm_attibutes = [] # [id, ego_time, ego_x, ego_y, ego_z, ego_yaw, ego_pitch, ego_roll, ego_speed]
    bsm_obj_time, bsm_obj_width = userData['V2X_BSM'].readHeader()   
    for i in range(bsm_obj_width):
        id,delay_time,x,y,z,yaw,pitch,roll,speed = userData['V2X_BSM'].readBody(i)
        bsm_attibutes.append([id,ego_time,x,y,z,yaw,pitch,roll,speed])
        
    # 读取RSM信息
    rsm_attibutes = []
    rsm_obj_time, rsm_obj_width = userData['V2X_RSM'].readHeader()
    for i in range(rsm_obj_width):
        id,delay_time,type,shape,x,y,z,yaw,pitch,roll,speed = userData['V2X_RSM'].readBody(i)
        rsm_attibutes.append([id,delay_time,type,shape,x,y,z,yaw,pitch,roll,speed])
    # print('V2X_RSM',rsm_obj_time, rsm_obj_width )

    # 读取RSI(trafficsign)信息
    rsi_attibutes = []
    rsi_obj_time, rsi_obj_width = userData['V2X_RSI'].readHeader()
    for i in range(rsi_obj_width):
        id,delay_time,shape,x,y,z,yaw,pitch,roll = userData['V2X_RSI'].readBody(i)
        rsi_attibutes.append([id,delay_time,shape,x,y,z,yaw,pitch,roll])  
    # print('V2X_RSI',rsi_obj_time, rsi_obj_width )
    
    # 读取MAP信息
    map_attibutes = []
    map_obj_time, map_obj_width = userData['V2X_MAP'].readHeader()
    for i in range(map_obj_width):
        id,delay_time = userData['V2X_MAP'].readBody(i)
        map_attibutes.append([id,delay_time])
    # print('V2X_MAP',map_obj_time, map_obj_width, map_attibutes)
    
    # 读取SPAT信息(交通信号灯基本信息)
    spat_obj_time, spat_obj_width = userData['V2X_SPAT'].readHeader()
    for i in range(spat_obj_width):
        id,delay_time,x,y,z,yaw,pitch,roll = userData['V2X_SPAT'].readBody(i)
    # print('V2X_SPAT',spat_obj_time, spat_obj_width)

    # 读取行人信息
    pedestrians = []
    participant_time, participant_width = userData["traffic"].getReader(userData["time"]).readHeader()
    
    for i in range(participant_width):
        id,type,shape,x,y,z,yaw,pitch,roll,speed= userData["traffic"].getReader(userData["time"]).readBody(i)
        if type==1:
            # print('x111y',x,y)
            pedestrians.append([id,type,shape,x,y,z,yaw,pitch,roll,speed])
            if str(id) in userData['pedestrians_points']:
                if len(userData['pedestrians_points'][str(id)])<20:
                    userData['pedestrians_points'][str(id)].append([id,ego_time,x,y,z,yaw,pitch,roll,speed])
                else:
                    userData['pedestrians_points'][str(id)].append([id,ego_time,x,y,z,yaw,pitch,roll,speed])   
                    del(userData['pedestrians_points'][str(id)][0])
            else:
                userData['pedestrians_points'][str(id)] = []

    PSMInfo = [basell,pedestrians,userData['pedestrians_points']] 
    psmData = Build_PSM.getPSMData(PSMInfo) 
    psmEncoded = ltevCoder_2.encode('PersonalSafetyMessage', psmData)
    # print('111111',psmEncoded)
    psmEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':15,'value':psmEncoded})) 
    # print('1111112',psmEncoded_2)
    psmDecoded_2 = ltevCoder_2.decode('MessageFrame',psmEncoded_2)
    psmDecoded = ltevCoder_2.decode('PersonalSafetyMessage',psmDecoded_2[1]['value'])  
    print('psmDecoded',psmDecoded)

    rtcmData = Build_RTCM.getRTCMData() 
    rtcmEncoded = ltevCoder_2.encode('RTCMcorrections', rtcmData)
    # print('111111',rtcmEncoded)
    rtcmEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':10,'value':rtcmEncoded})) 
    # print('1111112',rtcmEncoded_2)
    rtcmDecoded_2 = ltevCoder_2.decode('MessageFrame',rtcmEncoded_2)
    rtcmDecoded = ltevCoder_2.decode('RTCMcorrections',rtcmDecoded_2[1]['value'])  
    print('rtcmDecoded',rtcmDecoded)


    if len(pedestrians)>0:
        distance_between_predestrian_and_ego = math.sqrt(math.pow(abs(ego_x-pedestrians[0][0]),2)+math.pow(abs(ego_y-pedestrians[0][1]),2))
    else:
        distance_between_predestrian_and_ego = 1000
    
    #读取交通标志牌的信息:[(shape,x,y,z,yaw,pitch,roll)]
    traffic_signs = []
    traffic_signs = getTrafficSign(distance=200)
    
    #读取障碍物（水马）的 消息，为RSI数据包的rte字段服务:[(shape,x,y,z,yaw,pitch,roll)]
    obstacles = []
    obstacles = getObstacle(distance=200)        
    
    # 读取交通车的信息，并形成obu列表组表 [type,x,y,z,yaw,pitch,roll,speed]   同时获取所有交通参与者
    participants = []
    interface_cars = []
    obu_time, obu_width = userData["traffic"].getReader(userData["time"]).readHeader()
    
    for i in range(participant_width):
        id,type,shape,x,y,z,yaw,pitch,roll,speed= userData["traffic"].getReader(userData["time"]).readBody(i)
        participants.append([id,type,shape,x,y,z,yaw,pitch,roll,speed])
        if type==0:
            interface_cars.append([id,type,shape,x,y,z,yaw,pitch,roll,speed])
    obu_list = []
    obu_list.append(['ego', 000, 0, 38, ego_x, ego_y, ego_z, ego_yaw, ego_pitch, ego_roll, ego_speed])
    if len(interface_cars)>0:
        for veh in interface_cars: 
            veh.insert(0,'interface_car')
            obu_list.append(veh)

    
    #rsu列表组表 :[(shape,x,y,z,yaw,pitch,roll,fov,range)]
    rsu_list = []
    rsulist = getRSU(distance=500)
    for rsu in rsulist:
        rsu_list.append(rsu)
    
    
    hv_heading =  ((-ego_yaw + math.pi/2)*180/math.pi)
    if hv_heading >=360:
        hv_heading -= 360
    elif hv_heading < 0:
        hv_heading += 360
    
    # ssm消息的asn打包  
    # ltevCoder_2为2期打包器，同时支持一期数据打包（注意，二期数据分两级打包）
    ego = [ego_x, ego_y, ego_z, hv_heading, ego_pitch, ego_roll, ego_speed]
    ssmData = Build_SSM.OBUGetSSMData(basell,obu_list[1],ego,participants,traffic_signs,obstacles) 
    # print('ssmData',ssmData)
    ssmEncoded = ltevCoder_2.encode('SensorSharingMsg', SSM.PrepareForCode(ssmData))
    # print('111111',ssmEncoded)
    ssmEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':12,'value':ssmEncoded})) 
    # print('1111112',ssmEncoded_2)
    ssmDecoded_2 = ltevCoder_2.decode('MessageFrame',ssmEncoded_2)
    ssmDecoded = ltevCoder_2.decode('SensorSharingMsg',ssmDecoded_2[1]['value'])  
    print('SSM',ssmDecoded) 
    
    
    platoon_vehicles = [2,3,4,5]
    # pmm消息的asn打包
    pmmData = Build_PMM.getPMMData(platoon_vehicles) 
    pmmEncoded = ltevCoder_2.encode('CLPMM', pmmData)
    pmmEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':16,'value':pmmEncoded}))
    print('pmmEncoded_2',pmmEncoded_2) 
    pmmDecoded_2 = ltevCoder_2.decode('MessageFrame',pmmEncoded_2)
    pmmDecoded = ltevCoder_2.decode('CLPMM',pmmDecoded_2[1]['value'])  
    print('pmmDecoded',pmmDecoded) 
    
    # 解析用户提供的demo组队消息（来自于用户方面的OBU）
    demo_ = b'802a0010274c1919999998181819c9f4991999999818181980000000100000000c80001919999998181819a6'  #0400 8da0 002c
    demo_2 = binascii.a2b_hex(demo_)
    print('demo_',isinstance(demo_,bytes),len(demo_),demo_[0],demo_[1])
    print('demo_2',isinstance(demo_2,bytes),len(demo_2),demo_2[0],demo_2[1])
    pmmDecoded_2 = ltevCoder_2.decode('MessageFrame',demo_2)
    pmmDecoded = ltevCoder_2.decode('CLPMM',pmmDecoded_2[1]['value'])  
    print('pmmDecoded----------',pmmDecoded) 
    

    # VIR消息的asn打包
    ego_ = [ego_x, ego_y, ego_z, hv_heading, ego_pitch, ego_roll, ego_speed]
    taskRoute = getTaskRoute()  #[(edge, direction)]
    currentEdge = getCurrentEdge()  #edge
    currentEdgeLanes = getEdgeLanes(currentEdge)  #[lane]
    plan_pathPoints = getKeyPoints()   #[(x,y,type,lane)]
    userData['sl_ego'] += ego_speed*0.01  #(ego_time-userData['last'])/1000
    VIRInfo =  [basell,taskRoute,currentEdge,currentEdgeLanes,plan_pathPoints,userData['sl_ego']]
    # print('VIRInfo',VIRInfo) 
    virData = Build_VIR.getVIRData(ego_,participants,'HV','CIP',VIRInfo) 
    # print('virData',virData) 
    virEncoded = ltevCoder_2.encode('VehIntentionAndRequest', virData)
    virEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':13,'value':virEncoded}))
    # print('virEncoded_2',virEncoded_2) 
    virDecoded_2 = ltevCoder_2.decode('MessageFrame',virEncoded_2)
    virDecoded = ltevCoder_2.decode('VehIntentionAndRequest',virDecoded_2[1]['value'])  
    # print('ego',ego) 
    # print('ego_',ego_) 
    print('virDecoded',virDecoded) 
    
    
    # RSC消息的asn打包
    HV_Info = ego_
    RSCInfo =  [basell,taskRoute,currentEdge,currentEdgeLanes,plan_pathPoints,userData['sl_ego'],HV_Info]
    rscData = Build_RSC.getRSCData(rsulist[0],RSCInfo) 
    # print('rscData',rscData) 
    rscEncoded = ltevCoder_2.encode('RoadsideCoordination', rscData)
    rscEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':11,'value':rscEncoded}))
    # print('rscEncoded_2',rscEncoded_2) 
    rscDecoded_2 = ltevCoder_2.decode('MessageFrame',rscEncoded_2)
    rscDecoded = ltevCoder_2.decode('RoadsideCoordination',rscDecoded_2[1]['value'])  
    print('rscDecoded',rscDecoded) 



# 仿真实验结束时回调
def ModelTerminate(userData):
    pass
