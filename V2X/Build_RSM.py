import math
from .Message  import *
import datetime
import json


def getRSMData(rsu_info, participants):#interface_cars.append([id,type,shape,x,y,z,yaw,pitch,roll,speed])
    # 创建RSM消息帧
    RSM_msgCount = 0
    RSMData=MsgFrame.RSM_MsgFrame()
    try:
        earth_radius = 6371004
        RSM_msgCount += 1
        if RSM_msgCount>=127:
            RSM_msgCount = RSM_msgCount -127
        RSMData['msgCnt'] = RSM_msgCount
        # RSIData['id']=rsu_info.id
        RSMData['id']='00000001' #rsu暂时无ID属性，暂置为1
        lat = (rsu_info[2]) * 180.0 / (math.pi * earth_radius) + 39.5427 
        longi = ((rsu_info[1]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
        RSMData['refPos']['lat']=int(10000000 * lat)
        RSMData['refPos']['long']=int(10000000 * longi)
        RSMData['refPos']['elevation']=int(rsu_info[3])
        msg_participants=[]
        
        participant_list = []
        # vehs=self.g["VehicleDynamic"].copy()
        for item in participants:
            participant = {}
            participant['id'] = item[0]
            participant['type'] = item[2]
            participant['shape'] = item[3]
            participant['X'] = item[4]
            participant['Y']= item[5]
            participant['Z'] = item[6]
            participant['Yaw'] = item[7]
            participant['Pitch'] = item[8]
            participant['Roll'] = item[9]
            participant['Speed'] = item[10]
            participant_list.append(participant)

        id=1
        for v in participant_list: #需要新的数据源  
            dx=rsu_info[1]-v['X']
            dy=rsu_info[2]-v['Y']
            dz=rsu_info[3]-v['Z']
            dis=math.sqrt((dx**2)+(dy**2)+(dz**2))
            if(dis > 200): 
                continue
            p=RSM.RSMParticipantData_DF()
            p['ptcId']=id
            id=id+1
            p['ptcType']=1
            # print('v[type]',v['type'])
            if(v['type']==1):
                p['ptcType']=3
            p['id']='00000' +str(v['id'])
            v_lat = (v['Y']) * 180.0 / (math.pi * earth_radius) + 39.5427 
            v_longi = ((v['X']) * 180.0 / (math.pi * earth_radius)) / math.cos(v_lat * math.pi / 180.0) + (116.2317)
            p['pos']['offsetLL']=('position-LatLon', {'lon':int(10000000 * v_longi), 'lat':int(10000000 * v_lat)})
            p['pos']['offsetV']=('elevation', int(v['Z']))
            p['speed']=int(v['Speed']/0.02)
            p['heading']=v['Yaw']
            rsm_yaw =round(v['Yaw'],4)-math.pi/2
            if rsm_yaw<0:
                rsm_yaw = 2*math.pi-math.fabs(rsm_yaw)
            rsm_yaw = math.fabs(rsm_yaw-2*math.pi)  
            rsm_yaw2 = int(round((rsm_yaw*180/3.14)/0.0125)) 
            p['heading']=rsm_yaw2
            if p['heading'] > 359.9875/0.0125:
                p['heading'] -= 359.9875/0.0125
            p['heading'] = int(p['heading'] )
            # p['secMark']= int((self.scheduler.currentTime/1000-int(self.scheduler.currentTime/1000))*60000) # self.scheduler.currentTime/1000            
            p['secMark']=int((datetime.datetime.utcnow().timestamp()%60)*1000)
            
            msg_participants.append(p)
        RSMData['participants']=msg_participants
        # self.param['congested']=id>5

    except Exception as ex:
        print(ex)
        return RSMData
    else:
        return RSMData
