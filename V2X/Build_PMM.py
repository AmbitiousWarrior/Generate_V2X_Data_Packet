import math
from .Message  import *
import datetime
import json
import os
#获取文件父目录
Agent_V2X_Dir = os.path.dirname(__file__)


def getPMMData(vehicles):
    # 创建RSI消息帧
    PMM_msgCount = 0
    PMMData=MsgFrame.PMM_MsgFrame()
    try:
        PMM_msgCount += 1
        if PMM_msgCount>=127:
            PMM_msgCount = PMM_msgCount -127

        PMMData['msgCnt'] = PMM_msgCount
        PMMData['id']='1' #rsu暂时无ID属性，暂置为1
        PMMData['secMark']=int((datetime.datetime.utcnow().timestamp()%60)*1000)
        PMMData['pid']=vehicles[0]
        PMMData['role'] = 0
        PMMData['status'] = 0
        
        PMMData['leadingExt'] = {}
        PMMData['leadingExt']['memberList'] = [vehicles[1],vehicles[2],vehicles[3],vehicles[4]] 
        PMMData['leadingExt']['joiningList'] = []
        PMMData['leadingExt']['leavingList'] = []
        PMMData['leadingExt']['capacity'] = 10
        PMMData['leadingExt']['openToJoin'] = 1



    except Exception as ex:
        print(ex)
        return PMMData
 
    return PMMData



