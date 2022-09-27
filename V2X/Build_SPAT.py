import math
# from Message  import *
from V2X.Message  import *
import datetime
import json
# import trafficlight_phases
import V2X.trafficlight_phases



SPAT_msgCount = 0
def getSPATData(ego_time):
    # print('=============',ego_time)
    # 创建SPAT消息帧
    SPATData=MsgFrame.SPAT_MsgFrame()
    try:      
        global SPAT_msgCount
        SPAT_msgCount += 1
        if SPAT_msgCount>=127:
            SPAT_msgCount = SPAT_msgCount -127
        SPATData['msgCnt'] = SPAT_msgCount
        SPATData['name']='trafficlight01'
        SPATData['timeStamp']=int((datetime.datetime.utcnow().timestamp()%60))

        now_time = int(ego_time/100) % 1370
        SPATData['intersections'].append(V2X.trafficlight_phases.creat_intersection_phases(now_time+300)) 
        

    except Exception as ex:
        print(ex)
        return SPATData

    # SPATData_json = json.dumps(SPATData)
    # with open('C:\\Users\\15751002165\\Desktop\\SPAT_message.txt','w') as FD:
    #     FD.write(SPATData_json)
    return SPATData
