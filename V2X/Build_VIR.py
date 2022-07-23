import math
from .Message  import *
import datetime
import json
import os
#获取文件父目录
Agent_V2X_Dir = os.path.dirname(__file__)


def getVIRData(ego,rsu_info, traffic_signs_info, *obstacles):
    # 创建VIR消息帧
    VIR_msgCount = 0
    VIRData=MsgFrame.VIR_MsgFrame()
    try:
        earth_radius = 6371004
        RSI_msgCount += 1
        if RSI_msgCount>=127:
            RSI_msgCount = RSI_msgCount -127

        VIRData['msgCnt'] = RSI_msgCount
        # RSIData['id']=rsu_info.id
        VIRData['id']='001' #temperary vehicle ID   same as id in BSM
        # RSIData['moy']=int(self.scheduler.currentTime/1000)  
        VIRData['secMark']=int((datetime.datetime.utcnow().timestamp()%60)*1000)
        
        lat = (ego[1]) * 180.0 / (math.pi * earth_radius) + 37.788204
        longi = ((ego[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (-122.399498)
        VIRData['refPos']['lat']=int(10000000 * lat)
        VIRData['refPos']['long']=int(10000000 * longi)
        VIRData['refPos']['elevation']=int(ego[2])


        pathPlanningPoint_currentPos = VIR.pathPlanningPoint()
        pathPlanningPoint_currentPos['posInMap'] ['upstreamNodeId']=0
        pathPlanningPoint_currentPos['posInMap'] ['downstreamNodeId']=0
        
        
        VIRData['intAndReq']['currentPos'] = pathPlanningPoint_currentPos
        
        
        
        if(len(traffic_signs_info)>0):         
            for info in traffic_signs_info:
                RSIPoint=RSI.RSIPathPoint_DF()
                lat = (info[4]) * 180.0 / (math.pi * earth_radius) + 37.788204
                longi = ((info[3]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (-122.399498)
                RSIPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat)})
                RSIPathData['activePath'].append(RSIPoint)


                RTSData=RSI.RTSData_DF()            
                # for k in RSIAlertType.keys(): 
                #     if(self.param['owner3D'].Unity_Resource.lower().find(k.lower())>0):
                #         RTSData['signType']=RSIAlertType[k]  
                for (k,v) in RSIAlertType_5.items():
                    if v==info[2]:     
                        if k in RSIAlertType:          
                            RTSData['signType']=RSIAlertType[k]     
                    else:
                        RTSData['signType']=0
                RTSData['referencePaths'].append(RSIPathData)
                
                #ludayong 20211208 当rtss的referenceLinks为空时，将该字段从主包中删除    
                if len(RTSData['referenceLinks']) == 0:  
                        RTSData.pop('referenceLinks')
                        
                RTSData['signPos']['offsetLL']=('position-LatLon', {'lon':RSIData['refPos']['long'], 'lat':RSIData['refPos']['lat']})
                RTSData['signPos']['offsetV'] = ('elevation', 0)
                RSIData['rtss'].append(RTSData)
        
        # 依然由水马进行rte事件的位置标识
        rte_object = [0.0,0.0,0]
        for obstacle in obstacles:
            if(obstacle[0][0] == 4):                    
                rte_object = [obstacle[0][2],obstacle[0][1],obstacle[0][3]]
        
        try:
            # configurationpath='.'+ '\\' + r'static_configuration.json'
            configurationpath=Agent_V2X_Dir + '\\' + r'static_configuration.json'
            configurationFile = open(configurationpath,"rb")
            configuration = json.load(configurationFile)
        except FileNotFoundError:
            print("-----static_configuration.json doesn't exist-----")
    
        if configuration:
            if configuration["RSU"]["RSI"]["RTE"]!=None:
                RTEData=RSI.RTEData_DF() 
                RTEData['eventType']=configuration["RSU"]["RSI"]["RTE"]["eventType"]
                lat = (rte_object[0]) * 180.0 / (math.pi * earth_radius) + 37.788204
                longi = ((rte_object[1]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (-122.399498)
                RTEData['eventPos']['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat)})
                RTEData['eventPos']['offsetV'] = ('elevation', 0)
                RTEPathData=RSI.ReferencePath_DF()
                for i in range(5):
                    RTEPoint=RSI.RSIPathPoint_DF()
                    lat = (rte_object[0]) * 180.0 / (math.pi * earth_radius) + 37.788204
                    longi = ((rte_object[1]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (-122.399498)
                    if i == 0:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi-1*5400), 'lat':int(10000000 * lat)})
                    if i == 1:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi+1*5400), 'lat':int(10000000 * lat)})
                    if i == 2:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat)})
                    if i == 3:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat-1*5400)})
                    if i == 4:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat+1*5400)})
                    RTEPathData['activePath'].append(RTEPoint)
                RTEData['referencePaths'].append(RTEPathData)
                RTEData.pop('referenceLinks')
                RSIData['rtes'].append(RTEData)
        
        #ludayong 20211117 当rtes为空，将该字段从主包中删除    
        if len(RSIData['rtes']) == 0:  
                RSIData.pop('rtes')

    except Exception as ex:
        print(ex)
        return RSIData
    # self.param['rsiFrame']=RSIData
    return RSIData




