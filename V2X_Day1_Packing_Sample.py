#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   aeb.py
@Time    :   2021/08/13
@Author  :   hf
@Version :   1.0
'''

import mmap
from pickle import FALSE
import re
import threading
import numpy as np
# from paramiko import Agent
from DataInterfacePython import *
import math
from xml.dom.minidom import parseString
import dicttoxml
from V2X.Message import *
from V2X import OBU
from V2X import RSU
from V2X import Build_BSM
from V2X import Build_RSI
from V2X import Build_RSM
from V2X import Build_SPAT
from V2X import Build_SSM
from V2X import V2X_UDP
import base64
import sys
import datetime
import json
import asn1tools
import os
from socket import *
#获取文件父目录
Agent_V2X_Dir = os.path.dirname(__file__)
 
ltevCoder = None
ltevCoder_2 = None

def Warning(userData,level,warn):
    bus = userData["warning"].getBus()
    size = userData["warning"].getHeaderSize()
    bus[size:size + len(warn)] = '{}'.format(warn).encode()
    userData["warning"].writeHeader(*(userData["time"], level, len(warn)))

def VehicleControl(userData, valid, throttle, brake, steer, mode, gear):
    userData['ego_control'].writeHeader(*(userData['time'], valid, throttle, brake, steer, mode, gear))


def calc_crc16(data: bytes):#查表法
    '''
    CRC-16 (CCITT) implemented with a precomputed lookup table
    '''
    table = [ 
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7, 0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6, 0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485, 0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4, 0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
        0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823, 0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
        0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12, 0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
        0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41, 0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
        0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70, 0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
        0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F, 0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E, 0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D, 0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C, 0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB, 0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
        0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A, 0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
        0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9, 0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
        0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8, 0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
    ]
    
    crc = 0x0000
    for byte in data:
        crc = (crc << 8) ^ table[(crc >> 8) ^ byte]
        crc &= 0xFFFF                                   # important, crc must stay 16bits all the way through
    return crc
             



# 仿真实验启动时回调
def ModelStart(userData):
    # 构造雷达总线读取器
    userData['Radar'] = BusAccessor(userData['busId'], 'Radar_ObjList_G.0','time@i,64@[,OBJ_ID@i,OBJ_Class@d,OBJ_Azimuth@d,OBJ_Elevation@d,OBJ_Velocity@d,OBJ_Range@d,OBJ_RCS@d')
    # 构造车道线传感器总线读取器
    userData['Laneline'] = BusAccessor(userData['busId'], 'MonoDetector_Lane.0',
                                       "Timestamp@i,4@[,Lane_ID@i,Lane_Distance@d,Lane_Car_Distance_Left@d,Lane_Car_Distance_Right@d,Lane_Curvature@d,Lane_Coefficient_C0@d,Lane_Coefficient_C1@d,Lane_Coefficient_C2@d,Lane_Coefficient_C3@d,Lane_Class@b")
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
        
        
    userData['letters'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    # 初始化变量，推荐使用此方法定义对于Agent的全局变量
    userData['last'] = 0
    userData['Vx'] = []
    userData['Time'] = []
    userData['i_term_last'] = 0
    userData['v_error_last'] = 0
    userData['steer'] = []
    # userData['udp_server1'] = V2X_UDP.ServerUDP()
    # userData['udp_server1'].start()
    # userData['udp_server2'] = V2X_UDP.ServerUDP()
    # userData['udp_server2'].start()
    
    # 创建socket
    tcp_client_socket = socket(AF_INET, SOCK_STREAM)
    # 目的信息
    # server_ip = '192.168.0.155'
    # server_port = 7777
    server_ip = '192.168.10.10'
    server_port = 8888
    # # 链接服务器
    # tcp_client_socket.connect((server_ip, server_port))
    # print(tcp_client_socket)
    # userData['tcp_client1'] =  tcp_client_socket


    
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
    print('111111111111111',userData['global9'].readHeader()[1],(int(userData['global9'].readHeader()[1])&0x30),(int(userData['global9'].readHeader()[1])&0x30)>>4)
    # 读主车车辆状态
    ego_time, ego_x, ego_y, ego_z, ego_yaw, ego_pitch, ego_roll, ego_speed = userData['ego_state'].readHeader()
    _, valid_last, throttle_last, brake_last, steer_last, mode_last, gear_last = userData['ego_control'].readHeader()
    _, VX, VY, VZ, AVx, AVy, AVz, Ax, Ay, Az, AAx, AAy, AAz = userData['ego_extra'].readHeader()
    if ego_time > userData['last']:
        userData['last'] = ego_time
    


    userData['mm'].seek(0)
    userData['mm'].write(int(ego_time).to_bytes(4, byteorder="little"))
    print('write//////////',int(ego_time).to_bytes(4, byteorder="little"),ego_time)
    time,lane,station,lateral,internal,nextJunction = userData['ego_traffic'].readHeader()
    print('ego_traffic',time,lane,station,lateral,internal,nextJunction)
    userData['mm'].seek(4)
    userData['mm'].write(int(lane).to_bytes(4, byteorder="little"))
    

    
               
    # 读车道线传感器信息，lane_a, lane_b, lane_c, lane_d三次多项式系数降幂排列, y = a*x^3 + b*x^2 + c*x + d
    lane_time, lane_width = userData['Laneline'].readHeader()
    lane_coefs = []
    lane_types = []
    for i in range(lane_width):
        Lane_ID, Lane_Distance, Lane_Car_Distance_Left, Lane_Car_Distance_Right, Lane_Curvature, Lane_Coefficient_C0, Lane_Coefficient_C1, Lane_Coefficient_C2, Lane_Coefficient_C3, Lane_Class = \
        userData['Laneline'].readBody(i)
        lane_coefs.append([Lane_Coefficient_C3, Lane_Coefficient_C2, Lane_Coefficient_C1, Lane_Coefficient_C0])

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
    print('V2X_RSM',rsm_obj_time, rsm_obj_width )
    # print('V2X_RSM0000000000000000000',rsm_attibutes)
    # 读取RSI(trafficsign)信息
    rsi_attibutes = []
    rsi_obj_time, rsi_obj_width = userData['V2X_RSI'].readHeader()
    for i in range(rsi_obj_width):
        id,delay_time,shape,x,y,z,yaw,pitch,roll = userData['V2X_RSI'].readBody(i)
        rsi_attibutes.append([id,delay_time,shape,x,y,z,yaw,pitch,roll])  
    print('V2X_RSI',rsi_obj_time, rsi_obj_width )
    
    # 读取MAP信息
    map_obj_time, map_obj_width = userData['V2X_MAP'].readHeader()
    for i in range(map_obj_width):
        id,delay_time = userData['V2X_MAP'].readBody(i)
    print('V2X_MAP',map_obj_time, map_obj_width )
    
    # 读取SPAT信息(交通信号灯基本信息)
    spat_obj_time, spat_obj_width = userData['V2X_SPAT'].readHeader()
    for i in range(spat_obj_width):
        id,delay_time,x,y,z,yaw,pitch,roll = userData['V2X_SPAT'].readBody(i)
    print('V2X_SPAT',spat_obj_time, spat_obj_width )

    # 读取行人信息
    pedestrians = []
    participant_time, participant_width = userData["traffic"].getReader(userData["time"]).readHeader()
    
    for i in range(participant_width):
        id,type,shape,x,y,z,yaw,pitch,roll,speed= userData["traffic"].getReader(userData["time"]).readBody(i)
        if type==1:
            pedestrians.append([x,y,z,yaw])
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
    
    
    
    # ssm消息的asn打包  
    # ltevCoder_2为2期打包器，同时支持一期数据打包（注意，二期数据分两级打包）
    ego = [ego_x, ego_y, ego_z, ego_yaw, ego_pitch, ego_roll, ego_speed]
    ssmData = Build_SSM.OBUGetSSMData(obu_list[1],ego,participants,traffic_signs,obstacles) 
    # ssmData.pop('rtes')
    # ssmData.pop('participants')
    # ssmData.pop('detectedRegion')
    # ssmData.pop('sensorPos')
    # ssmData.pop('equipmentType')
    # ssmData.pop('secMark')
    # ssmData.pop('id')
    
    # print('555',ssmData)
    # print('1111110000000',isinstance(ssmData,dict),isinstance(SSM.PrepareForCode(ssmData),dict),SSM.PrepareForCode(ssmData))
    # print('0000000',SSM.PrepareForCode(ssmData))
    
    ssmEncoded = ltevCoder_2.encode('SensorSharingMsg', SSM.PrepareForCode(ssmData))
    # print('111111',ssmEncoded)
    ssmEncoded_2 = ltevCoder_2.encode('MessageFrame',('msgFrameExt',{'messageId':12,'value':ssmEncoded})) 
    # print('1111112',ssmEncoded_2)

    

    global ltevCoder #一期asn打包器
    # BSM组包
    #在这里组主车的BSM包(就是将list转化为字典，使组包时变量的含义更加直观)，交通车的BSM包也同样处理
    veh_information = {}# id, ego_time, ego_x, ego_y, ego_z, ego_yaw, ego_pitch, ego_roll, ego_speed
    veh_information['ID'] = "001"#指主车 其他车辆使用veh_information['ID']= bsm_attibutes[i][0]
    veh_information['Time'] = ego_time
    veh_information['X'] = ego_x
    veh_information['Y'] = ego_y
    veh_information['Z'] = ego_z
    veh_information['Yaw'] = ego_yaw
    veh_information['Pitch'] = ego_pitch
    veh_information['Roll'] = ego_roll
    veh_information['Speed'] = ego_speed
    bsm_msg = Build_BSM.getBSMData(veh_information)
    bsmFrame = ('bsmFrame', BSM.PrepareForCode(bsm_msg))
    bsmEncoded = ltevCoder_2.encode('MessageFrame', bsmFrame)#type(bsmEncoded)=='bytearray'
    # print('0000000',isinstance(bsm_msg,dict),isinstance(bsm_msg,bytearray))
    # print('1111110000000',bsmFrame)
    # print('1111111111111222222',bsmEncoded)
    
    
    # rsm_msg = Build_RSM.getRSMData(rsulist[0],participants)
    if len(rsm_attibutes)>0:
        rsm_msg = Build_RSM.getRSMData(rsulist[0],rsm_attibutes)
        rsmFrame = ('rsmFrame', RSM.PrepareForCode(rsm_msg))
        rsmEncoded = ltevCoder.encode('MessageFrame', rsmFrame)
        # print('2222220000000',rsmFrame)
        # print('2222222222222',rsmEncoded)
    
    
    # print('333000',traffic_signs) #[(shape,x,y,z,yaw,pitch,roll)]
    # print('333333',rsi_attibutes) #id, delaytime, shape, x, y, z, yaw, pitch, roll, speed
    # rsi_msg = Build_RSI.getRSIData(rsulist[0],traffic_signs,obstacles)  
    if len(rsi_attibutes)>0:
        rsi_msg = Build_RSI.getRSIData(rsulist[0],rsi_attibutes,obstacles)
        # print('rsi_msg',rsi_msg)  
        rsiFrame = ('rsiFrame', RSI.PrepareForCode(rsi_msg))
        # print('33333330000000',rsiFrame)
        rsiEncoded = ltevCoder.encode('MessageFrame', rsiFrame)
        # print('33333333333333',rsiEncoded)
    
    
    if spat_obj_width>0:
        spat_msg = Build_SPAT.getSPATData(ego_time)
        spatFrame = ('spatFrame', SPAT.PrepareForCode(spat_msg))
        # print('44444440000000',spatFrame)
        spatEncoded = ltevCoder.encode('MessageFrame', spatFrame)
        # print('44444444444444',spatEncoded)
    
        

    file = open('C:\\Users\\15751002165\\Desktop\\MAP_message_5.06.txt','r')  #打开文件
    file_data = file.readlines() #读取所有行
    # print(isinstance(file_data,(list)),'9999999999999999999')
    map_msg = eval(str(file_data[0]))
    # print(map_msg)
  
    mapFrame = ('mapFrame', MAP.PrepareForCode(map_msg))
    # print('55555550000000',mapFrame)
    
    
    beforexml = dicttoxml.dicttoxml(mapFrame,custom_root='MessageFrame',attr_type=False)
    xml = beforexml.decode('utf-8')
    dom = parseString(xml)
    prexml = dom.toprettyxml(indent='   ')#空格为缩进长度
    f = open('C:\\Users\\15751002165\\Desktop\\MAP_message_5.04.xml','w',encoding='utf-8')
    f.write(prexml)
    f.close()
        
    for item1 in mapFrame[1]['nodes']:   
        if len(item1['inLinks'])<4:
            item1.pop('inLinks')
        else:
            for item2 in item1['inLinks']: 
                for item3 in item2['lanes']:
                    if len(item3['connectsTo'])==0:                                        
                        item3.pop('connectsTo')
                if len(item2['movements'])==0: #去除可能存在的空字段的影响 
                    item2.pop('movements')
            for item2 in item1['inLinks']:         
                if len(item2['lanes'])==0:
                    MapLane=MAP.MapLane_DF()
                    MapLane.pop('laneAttributes')
                    MapLane.pop('maneuvers')
                    MapLane.pop('connectsTo')
                    MapLane.pop('points')
                    MapLane.pop('speedLimits')
                    item2['lanes'].append(MapLane) 
                                       
    if map_obj_width>0:                
        mapEncoded = ltevCoder.encode('MessageFrame', mapFrame)
        # print('55555555555555',mapEncoded)
        # print('66666666666666',sys.getsizeof(mapEncoded))
        

# 仿真实验结束时回调
def ModelTerminate(userData):
    # userData['tcp_client1'].close()
    pass
