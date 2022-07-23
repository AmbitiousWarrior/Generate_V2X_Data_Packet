import math
from .Message  import *
import datetime
import json
import os 


import os
#获取文件父目录
Agent_V2X_Dir = os.path.dirname(__file__)

BSM_msgCount = 0
earth_radius = 6371004  # 地球半径
def getBSMData(veh_information):#需要新的数据源
    # 创建BSM消息帧
    BSMData=MsgFrame.BSM_MsgFrame()
    try:
        configurationpath=Agent_V2X_Dir + '\\' + r'static_configuration.json'
        # print('===============',configurationpath)
        # configurationpath='.' + '\\' + r'static_configuration.json'
        configurationFile = open(configurationpath,"rb")
        configuration = json.load(configurationFile)
    except FileNotFoundError:
        print("-----static_configuration.json doesn't exist-----")
    try:
        #EARTH_RADIUS=6371004
        #ORIGIN_LAT=37.788204
        #ORIGIN_ELE=0.0
        #ORIGIN_LON=-122.399498
        earth_radius = 6371004
        # 通过节点所有者标识符，获取主车数据
        ego=veh_information  #将主车的信息赋予ego
        # 拼接BSM数据
        BSMData['id']=ego['ID']

        global BSM_msgCount
        BSM_msgCount += 1
        if BSM_msgCount>=127:
            BSM_msgCount = BSM_msgCount -127
        BSMData['msgCnt'] = BSM_msgCount
        
        lat = (ego['Y']) * 180.0 / (math.pi * earth_radius) + 37.788204
        # Longitude is in 1/10 micro degrees in BSM frame - long %
        longi = ((ego['X']) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (-122.399498)
        BSMData['pos']['long']=10000000 * longi
        BSMData['pos']['lat']=10000000*lat
        BSMData['pos']['elevation']=0.0
        BSMData['secMark']=int((datetime.datetime.utcnow().timestamp()%60)*1000)
        BSMData['speed']=round(ego['Speed']/0.02)
        
        bsm_yaw =round(ego['Yaw'],4)-math.pi/2
        if bsm_yaw<0:
            bsm_yaw = 2*math.pi-math.fabs(bsm_yaw)
        bsm_yaw2 = math.fabs(bsm_yaw-2*math.pi)    
        BSMData['heading']=round((bsm_yaw2*180/3.14)/0.0125)
        if BSMData['heading'] > 359.9875:
            BSMData['heading'] -=359.9875 

        BSMData['accelSet']['long']= 0.0
        BSMData['accelSet']['lat']= 0.0
        BSMData['accelSet']['vert']=0.0
        BSMData['accelSet']['yaw']=0.0
        BSMData['size']['width']=180 * 100 # in unit of 1 cm
        BSMData['size']['length']=500 * 100 # in unit of 1 cm
        BSMData['size']['height']=1.52 * (100/5)
        BSMData['vehicleClass']['classification']=10


        light_status_list = []
        if configuration:
            for k,v in configuration['HV_1']['Body']['light'].items():
                if v['Start_time'] < ego['Time']  and ego['Time']  < v['End_time']:
                    light_status_list.append(v['Light_status'])
                else:
                    light_status_list.append(0)

            lights=[0,0]
            lights[0]=128*light_status_list[0]+64*light_status_list[1]+32*light_status_list[2]+16*light_status_list[3]+8*light_status_list[4]+4*light_status_list[5]+2*light_status_list[6]+light_status_list[7]
            lights[1]=128*light_status_list[8]
            BSMData['safetyExt']['lights'][0]=lights

            temp_json1 = configuration['HV_2']['Body']['Out-of-control_vehicle_condition']
            if temp_json1['brakePadel']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['brakePadel']['End_time']:
                BSMData['brakes']['brakePadel']=temp_json1['brakePadel']['brakePadel_status']

            if temp_json1['wheelBrakes']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['wheelBrakes']['End_time']:
                temp_wB=temp_json1['wheelBrakes']['wheelBrakes_status']
                wheelBrakes=[0]
                if temp_wB['unavailable'] != 0:
                    wheelBrakes[0] = 0
                    BSMData['brakes']['wheelBrakes'][0] = wheelBrakes
                else:
                    wheelBrakes[0] = (temp_wB['unavailable']*16+temp_wB['leftFront']*8+temp_wB['leftRear']*4+temp_wB['rightFront']*2+temp_wB['rightRear'])*8
                    BSMData['brakes']['wheelBrakes'][0] = wheelBrakes

            if temp_json1['traction']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['traction']['End_time']:
                BSMData['brakes']['traction']=temp_json1['traction']['traction_status']

            if temp_json1['abs']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['abs']['End_time']:
                BSMData['brakes']['abs']=temp_json1['abs']['abs_status']

            if temp_json1['scs']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['scs']['End_time']:
                BSMData['brakes']['scs']=temp_json1['scs']['scs_status']

            if temp_json1['brakeBoost']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['brakeBoost']['End_time']:
                BSMData['brakes']['brakeBoost']=temp_json1['brakeBoost']['brakeBoost_status']

            if temp_json1['auxBrakes']['Start_time'] < ego['Time']  and ego['Time']  < temp_json1['auxBrakes']['End_time']:
                BSMData['brakes']['auxBrakes']=temp_json1['auxBrakes']['auxBrakes_status']
            events=[0,0]
            if temp_json1['abs']['abs_status'] == 3 or temp_json1['abs']['abs_status'] == 2:
                abs_status = 1
            else:
                abs_status = 0
            if temp_json1['traction']['traction_status'] == 3 or temp_json1['traction']['traction_status'] == 2:
                traction_status = 1
            else:
                traction_status = 0
            if temp_json1['scs']['scs_status'] == 3 or temp_json1['scs']['scs_status'] == 2:
                scs_status = 1
            else:
                scs_status = 0
            if temp_json1['brakeBoost']['brakeBoost_status'] == 3 or temp_json1['brakeBoost']['brakeBoost_status'] == 2:
                brakeBoost_status = 1
            else:
                brakeBoost_status = 0
            events[0]=128*light_status_list[4]+64*0+32*abs_status+16*traction_status+8*scs_status+4*0+2*0+1*brakeBoost_status
            events[1]=0
            BSMData['safetyExt']['events'][0] = events
         
    except Exception as ex:
        print(ex)
        return BSMData
    else:
        # BSMData_json = json.dumps(BSMData)
        # with open('C:\\Users\\15751002165\\Desktop\\BSM_message.txt','w') as FD:
        #     FD.write(BSMData_json)
        return BSMData
