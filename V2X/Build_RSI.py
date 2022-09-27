import math
from .Message  import *
import datetime
import json
import os
#获取文件父目录
Agent_V2X_Dir = os.path.dirname(__file__)


def getRSIData(rsu_info, traffic_signs_info,pathpoints, *obstacles):
    # 创建RSI消息帧
    RSI_msgCount = 0
    RSIData=MsgFrame.RSI_MsgFrame()
    try:
        earth_radius = 6371004
        RSI_msgCount += 1
        if RSI_msgCount>=127:
            RSI_msgCount = RSI_msgCount -127

        RSIData['msgCnt'] = RSI_msgCount
        # RSIData['id']=rsu_info.id
        RSIData['id']='00000001'  #rsu暂时无ID属性，暂置为1
        # integer_id = int(1)
        # bytes_id= integer_id.to_bytes(8, 'big')            
        # RSIData['id']=bytes_id 
        # RSIData['moy']=int(self.scheduler.currentTime/1000)  
        RSIData['moy']=int((datetime.datetime.utcnow().timestamp()%60)) 
        
        lat = (rsu_info[2]) * 180.0 / (math.pi * earth_radius) + 39.5427 
        longi = ((rsu_info[1]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
        RSIData['refPos']['lat']=int(10000000 * lat)
        RSIData['refPos']['long']=int(10000000 * longi)
        RSIData['refPos']['elevation']=int(rsu_info[3])

        RSIPathData=RSI.ReferencePath_DF()
        if(len(traffic_signs_info)>0):         
            for info in traffic_signs_info:
                RSIPoint=RSI.RSIPathPoint_DF()
                RSIPoint_2 = RSI.RSIPathPoint_DF()
                # lat = (info[4]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                # longi = ((info[3]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                # RSIPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat)})
                # RSIPathData['activePath'].append(RSIPoint)
                # RSIPoint_2['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi + 5400), 'lat':int(10000000 * lat)})
                # RSIPathData['activePath'].append(RSIPoint_2)
                # print('pathpoints',pathpoints)

                pos1 =  pathpoints[0]  # [-400.0, -4.8]
                pos2 =  pathpoints[1]  # [-13.6, -4.8] 
                lat1 = (pos1[1]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                longi1 = ((pos1[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat1 * math.pi / 180.0) + (116.2317)

                lat2 = (pos2[1]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                longi2 = ((pos2[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat2 * math.pi / 180.0) + (116.2317)

                RSIPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi1), 'lat':int(10000000 * lat1)})
                RSIPathData['activePath'].append(RSIPoint)
                RSIPoint_2['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi2 + 1*5400), 'lat':int(10000000 * lat2)})
                RSIPathData['activePath'].append(RSIPoint_2)


                RTSData=RSI.RTSData_DF()            
                # for k in RSIAlertType.keys(): 
                #     if(self.param['owner3D'].Unity_Resource.lower().find(k.lower())>0):
                #         RTSData['signType']=RSIAlertType[k]  
                # for (k,v) in RSIAlertType_5.items():
                #     if v==info[2]:     
                #         if k in RSIAlertType:          
                #             # RTSData['signType']=RSIAlertType[k]    
                #             RTSData['signType']=85  
                #     else:
                #         RTSData['signType']=85
                RTSData['signType']=info[2]
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
                lat = (rte_object[0]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                longi = ((rte_object[1]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                RTEData['eventPos']['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat)})
                RTEData['eventPos']['offsetV'] = ('elevation', 0)
                RTEPathData=RSI.ReferencePath_DF()
                # for i in range(5):
                #     RTEPoint=RSI.RSIPathPoint_DF()
                #     lat = (rte_object[0]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                #     longi = ((rte_object[1]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                #     if i == 0:
                #         RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi-1*5400), 'lat':int(10000000 * lat)})
                #     if i == 1:
                #         RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi+1*5400), 'lat':int(10000000 * lat)})
                #     if i == 2:
                #         RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat)})
                #     if i == 3:
                #         RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat-1*5400)})
                #     if i == 4:
                #         RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi), 'lat':int(10000000 * lat+1*5400)})
                #     RTEPathData['activePath'].append(RTEPoint)
                for i in range(2):
                    RTEPoint=RSI.RSIPathPoint_DF()
                    pos1 =  pathpoints[0]  # [-400.0, -4.8]
                    pos2 =  pathpoints[1]  # [-13.6, -4.8] 
                    lat1 = (pos1[1]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                    longi1 = ((pos1[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat1 * math.pi / 180.0) + (116.2317)

                    lat2 = (pos2[1]) * 180.0 / (math.pi * earth_radius) + 39.5427 
                    longi2 = ((pos2[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat2 * math.pi / 180.0) + (116.2317)
                    if i == 0:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi1), 'lat':int(10000000 * lat1)})
                    if i == 1:
                        RTEPoint['offsetLL']=('position-LatLon', {'lon':int(10000000 * longi2), 'lat':int(10000000 * lat2)})

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


RSIAlertType={
    'Danger':37,'WXCU':37,'Rockfall':15,'Bangsha':15,'Turn':2,'FX':2,'ShiGong':38,'Slippy':17,'WetRoad':17,'Tunnel':21,'congested':1,
    'Jinzhi_1':201,'Jinzhi_2':202,'Jinzhi_3':203,'Jinzhi_4':204,'Jinzhi_5':205,'Jinzhi_6':206,'Jinzhi_7':207,'Jinzhi_8':208,
    'Jinzhi_9':209,'Jinzhi_10':210,'Jinzhi_11':211,'Jinzhi_12':212,'Jinzhi_13':213,'Jinzhi_14':214,'Jinzhi_15':215,'Jinzhi_16':216,
    'Jinzhi_17':217,'Base_DTLift':218,'Base_DT':219,'Base_LeftR':220,'Base_LeftR01':221,'Base_MultiPassenger':222,'Base_Parking001':223,
    'Base_Parking002':224,'Base_Parking003':225,'Base_Parking004':226,'Base_RightR':227,'Base_Transitlane':228,'Bangsha_1':15,
    'Bangsha_2':15,'CXC':231,'DB_1':232,'DB_2':233,'dulunm':234,'feijido_1':235,'feijido_2':236,'FX_1':237,'HELIU':238,'Jc_1':239,
    'Jc_2':240,'Jc_3':241,'Jc_4':242,'Jc_5':243,'Jc_6':244,'Jc_7':245,'Jc_8':246,'jysd':247,'lxxp':248,'SharpTurnLeft':2,
    'SharpTurnRight':2,'SHIGONG':251,'SHIGUYA':252,'SlipperySurfacejzo':253,'TD_1':254,'TD_2':255,'TD_3':256,'TD_4':257,'TFQ':258,
    #'Tunnel':259,'WXCU':260,
    'ZAI_1':261,'ZAI_2':262,'ZQQ_1':263,'ZYCJ':264,'十字':265,'HW_100mSign01':266,'HW_100mSign02':267,'HW_Compose01':268,
    'HW_Compose02':269,'HW_Compose03':270,'HW_DemarcationLine':271,'HW_Direction01':272,'HW_Direction02':273,'HW_Direction03':274,
    'HW_Disabled':275,'HW_ElectroniC01':276,'HW_ElectroniC02':277,'HW_Emergency':278,'HW_End':279,'HW_Entrance01':280,
    'HW_Entrance02':281,'HW_EntranceLD01':282,'HW_EntranceLD02':283,'HW_EntranceNotice01':284,'HW_EntranceNotice02':285,
    'HW_Exit':286,'HW_ExitLD':287,'HW_ExportNotice':288,'HW_Fewerlanes01':289,'HW_Fewerlanes02':290,'HW_FootBridge':291,
    'HW_Function01':292,'HW_Function02':293,'HW_Function03':294,'HW_Function04':295,'HW_Function05':296,'HW_Increaselanes':297,
    'HW_IntersectionA01 ':298,'HW_IntersectionA02 ':299,'HW_LD01':300,'HW_LD02':301,'HW_LinearGuidance01':302,'HW_LinearGuidance02':303,
    'HW_LinearGuidance03':304,'HW_LinearGuidance04':305,'HW_LocationDirection':306,'HW_LocationDistance':307,'HW_LocationR01':308,
    'HW_LocationR02':309,'HW_LocationR03':310,'HW_LocationR04':311,'HW_NextExit':312,'HW_ObservationTower':313,'HW_Parking01':314,
    'HW_Parking02':315,'HW_Parking03':316,'HW_Parking04':317,'HW_ParkingLane':318,'HW_ParkingTollLane01':319,'HW_ParkingTollLane02':320,
    'HW_ParkingTollLane03':321,'HW_ParkingTollLane04':322,'HW_PassingRound01':323,'HW_PassingRound02':324,'HW_RoadBrand01':325,
    'HW_RoadName':326,'HW_SpecialWeather':327,'HW_StopTicket':328,'HW_SubDistrict01':329,'HW_SubDistrict02':330,'HW_SubDistrict03':331,
    'HW_SubWay':332,'HW_Terminal01':333,'HW_Terminal02':334,'HW_TrafficInformation':335,'HW_TrafficMonitoring':336,'HW_Type01':337,
    'HW_Type02':338,'HW_Type03':339,'HW_VehicleDistance01':340,'HW_VehicleDistance02':341,'HW_VehicleDistance03':342,
    'HW_VehicleSpeed01':343,'HW_VehicleSpeed02':344,'HW_VehicleSpeed03':345,'HW_VehicleType01':346,'HW_VehicleType02':347,
    'HW_VehicleType03':348,'HW_VehicleType04':349,'HW_Weight':350
}

RSIAlertType_5={'Base_DTLift': 1, 'Base_DT': 2, 'Base_LeftR002': 3, 'Base_MultiPassenger': 4, 'Base_Parking001': 5, 'Base_Parking002': 6, 'Base_Parking003': 7, 'Base_Parking004': 8, 'Base_RightR': 9, 'Base_Transitlane': 10, 'Jinzhi_1': 11, 'Jinzhi_2': 12, 'Jinzhi_3': 13, 'Jinzhi_4': 14, 'Jinzhi_5': 15, 'Jinzhi_6': 16, 'Jinzhi_7': 17, 'Jinzhi_8': 18, 'Jinzhi_9': 19, 'Jinzhi_10': 20, 'Jinzhi_11': 21, 'Jinzhi_12': 22, 'Jinzhi_13': 23, 'Jinzhi_14': 24, 'Jinzhi_15': 25, 'Jinzhi_16': 26, 'Jinzhi_17': 27, 'JinzhiCC_28': 28, 'JinzhiCSTF_31': 29, 'JinzhiDDSL_13': 30, 'JinzhiDKC_06': 31, 'JinzhiDT_27': 32, 'JinzhiGD_34': 33, 'JinzhiHC_04': 34, 'JinzhiHC_14': 35, 'JinzhiJC_29': 36, 'JinzhiJDCTX_03': 37, 'JinzhiKD_33': 38, 'JinzhiLZC_12': 39, 'JinzhiMLB_32': 40, 'JinzhiMTC_11': 41, 'JinzhiNYC_10': 42, 'JinzhiRL_16': 43, 'JinzhiRX_15': 44, 'JinzhiSR_02': 45, 'JinzhiTC_17': 46, 'JinzhiTCGC_08': 47, 'JinzhiTF_30': 48, 'JinzhiTLJ_09': 49, 'JinzhiTX_01': 50, 'JinzhiXKC_07': 51, 'JinzhiXRTX_20': 52, 'JinzhiXS_24': 53, 'JinzhiJCXS_36': 54, 'rateLimiting80': 55, 'relief80': 56, 'JinzhiXZYW_22': 57, 'JinzhiXZZW_21': 58, 'JinzhiZHQC_05': 59, 'JinzhiZL_35': 60, 'JinzhiZX_23': 61, 'JinzhiZXCS_19': 62, 'JinzhiZXCX_18': 63, 'JinzhiZXYZ_26': 64, 'JinzhiZXZZ_25': 65, 'FreewayL_1': 66, 'FreewayL_2': 67, 'FreewayL_3': 68, 'FreewayL_4': 69, 'FreewayL_5': 70, 'FreewayL_6': 71, 'FreewayL_7': 72, 'FreewayL_8': 73, 'FreewayL_9': 74, 'FreewayL_10': 75, 'FreewayL_11': 76, 'FreewayL_12': 77, 'FreewayL_13': 78, 'FreewayL_14': 79, 'FreewayL_15': 80, 'FreewayL_16': 81, 'FreewayL_17': 82, 'FreewayL_17_01': 83, 'FreewayL_17_02': 84, 'FreewayL_18_01': 85, 'FreewayL_18_02': 86, 'FreewayL_19': 87, 'FreewayL_20': 88, 'FreewayL_21': 89, 'FreewayL_22': 90, 'FreewayL_23': 91, 'FreewayL_24_01': 92, 'FreewayL_24_02': 93, 'FreewayL_25': 94, 'FreewayL_26': 95, 'FreewayL_27': 96, 'FreewayL_28': 97, 'FreewayL_29': 98, 'FreewayL_30': 99, 'FreewayL_31': 100, 'FreewayL_32': 101, 'FreewayL_33': 102, 'FreewayL_34': 103, 'FreewayL_35': 104, 'FreewayL_36': 105, 'FreewayL_37_01': 106, 'FreewayL_37_02': 107, 'FreewayL_38_01': 108, 'FreewayL_38_02': 109, 'FreewayL_39_01': 110, 'FreewayL_39_02': 111, 'HW_100mSign01': 112, 'HW_100mSign02': 113, 'HW_Compose01': 114, 'HW_Compose02': 115, 'HW_Compose03': 116, 'HW_DemarcationLine': 117, 'HW_Disabled': 118, 'HW_ElectroniC01': 119, 'HW_ElectroniC02': 120, 'HW_Emergency': 121, 'HW_End': 122, 'HW_Entrance01': 123, 'HW_Entrance02': 124, 'HW_EntranceLD01': 125, 'HW_EntranceLD02': 126, 'HW_EntranceNotice01': 127, 'HW_EntranceNotice02': 128, 'HW_Exit': 129, 'HW_ExportNotice': 130, 'HW_FamousPlace': 131, 'HW_Fewerlanes01': 132, 'HW_Fewerlanes02': 133, 'HW_FootBridge': 134, 'HW_Function01': 135, 'HW_Function02': 136, 'HW_Function03': 137, 'HW_Function04': 138, 'HW_Function05': 139, 'HW_Increaselanes': 140, 'HW_LD02': 141, 'HW_LinearGuidance01': 142, 'HW_LinearGuidance02': 143, 'HW_LinearGuidance03': 144, 'HW_LinearGuidance04': 145, 'HW_LocationDistance': 146, 'HW_LocationR01': 147, 'HW_LocationR02': 148, 'HW_LocationR03': 149, 'HW_NextExit': 150, 'HW_ObservationTower': 151, 'HW_Parking02': 152, 'HW_Parking03': 153, 'HW_Parking04': 154, 'HW_ParkingLane': 155, 'HW_ParkingTollLane01': 156, 'HW_ParkingTollLane02': 157, 'HW_ParkingTollLane03': 158, 'HW_ParkingTollLane04': 159, 'HW_RoadBrand01': 160, 'HW_RoadName': 161, 'HW_SpecialWeather': 162, 'HW_StopTicket': 163, 'HW_SubDistrict01': 164, 'HW_SubDistrict02': 165, 'HW_SubWay': 166, 'HW_Terminal01': 167, 'HW_Terminal02': 168, 'HW_TrafficMonitoring': 169, 'HW_Type01': 170, 'HW_Type02': 171, 'HW_Type03': 172, 'HW_VehicleDistance01': 173, 'HW_VehicleDistance02': 174, 'HW_VehicleDistance03': 175, 'HW_VehicleSpeed01': 176, 'HW_VehicleSpeed02': 177, 'HW_VehicleSpeed03': 178, 'HW_VehicleType01': 179, 'HW_VehicleType02': 180, 'HW_VehicleType03': 181, 'HW_VehicleType04': 182, 'HW_Weight': 183, 'ZSBZ_001': 184, 'ZSBZ_002': 185, 'ZSBZ_003': 186, 'ZSBZ_004': 187, 'ZSBZ_005': 188, 'ZSBZ_006': 189, 'ZSBZ_007': 190, 'ZSBZ_008': 191, 'ZSBZ_009': 192, 'ZSBZ_010': 193, 'ZSBZ_011': 194, 'ZSBZ_012': 195, 'ZSBZ_013': 196, 'ZSBZ_014': 197, 'ZSBZ_015': 198, 'ZSBZ_016': 199, 'ZSBZ_017': 200, 'ZSBZ_018': 201, 'ZSBZ_019': 202, 'ZSBZ_021': 203, 'ZSBZ_022': 204, 'ZSBZ_023': 205, 'ZSBZ_024': 206, 'ZSBZ_025': 207, 'ZSBZ_026': 208, 'ZSBZ_027': 209, 'ZSBZ_028': 210, 'ZSBZ_029': 211, 'Bangsha_1': 212, 'Bangsha_2': 213, 'CXC': 214, 'DB_1': 215, 'DB_2': 216, 'dulunm': 217, 'feijido_1': 218, 'feijido_2': 219, 'FX_1': 220, 'FX_2': 221, 'HELIU': 222, 'Jc_1': 223, 'Jc_2': 224, 'Jc_3': 225, 'Jc_4': 226, 'Jc_5': 227, 'Jc_6': 228, 'Jc_7': 229, 'Jc_8': 230, 'Jc_9': 231, 'jysd': 232, 'lxxp_1': 233, 'SharpTurnLeft': 234, 'SharpTurnRight': 235, 'SHIGONG': 236, 'SHIGUYA': 237, 'TD_1': 238, 'TD_2': 239, 'TD_3': 240, 'TD_4': 241, 'TFQ': 242, 'Tunnel': 243, 'Warning_1': 244, 'Warning_2': 245, 'Warning_3': 246, 'Warning_4': 247, 'Warning_5': 248, 'Warning_6': 249, 'Warning_7': 250, 'Warning_8': 251, 'Warning_10': 252, 'Warning_11': 253, 'Warning_12': 254, 'Warning_13': 255, 'Warning_14': 256, 'Warning_15': 257, 'Warning_16': 258, 'Warning_17': 259, 'Warning_18': 260, 'Warning_19': 261, 'Warning_20': 262, 'WetRoad': 263, 'WXCU': 264, 'ZAI_1': 265, 'ZAI_2': 266, 'ZQQ_1': 267, 'ZYCJ': 268, 'fuzhubiaozhiBSSJ_01': 269, 'fuzhubiaozhiBSSJ_02': 270, 'fuzhubiaozhiBSXSFX_01': 271, 'fuzhubiaozhiBSXSFX_02': 272, 'fuzhubiaozhiBSXSFX_03': 273, 'fuzhubiaozhiBSXSFX_04': 274, 'fuzhubiaozhiBSXSFX_05': 275, 'fuzhubiaozhiBSXSFX_06': 276, 'fuzhubiaozhiBSXSFX_07': 277, 'fuzhubiaozhiBSXSFX_08': 278, 'fuzhubiaozhiCGGQCW': 279, 'fuzhubiaozhiEHLQYN': 280, 'fuzhubiaozhiHC': 281, 'fuzhubiaozhiHCTLJ': 282, 'fuzhubiaozhiHG': 283, 'fuzhubiaozhiJDC': 284, 'fuzhubiaozhiJHSDCD5KM': 285, 'fuzhubiaozhiJLCXSLX': 286, 'fuzhubiaozhiJLQFSD200M': 287, 'fuzhubiaozhiSG': 288, 'fuzhubiaozhiSRZS': 289, 'fuzhubiaozhiTF': 290, 'fuzhubiaozhiXCTKD': 291, 'fuzhubiaozhiXQ200M': 292, 'fuzhubiaozhiXX': 293, 'fuzhubiaozhiXZ100M': 294, 'fuzhubiaozhiXY100M': 295, 'fuzhubiaozhiXZXYG50M': 296, 'fuzhubiaozhiZHFZBZ': 297, 'gaoshibiaozhiDXCKY': 298, 'gaoshibiaozhiJAQD': 299, 'gaoshibiaozhiJSSJZSCDH': 300, 'gaoshibiaozhiJWJSXY': 301, 'gaoshibiaozhiJWJSXZ': 302, 'gaoshibiaozhiJWXPJSXY': 303, 'gaoshibiaozhiJWXPJSXZ': 304, 'gaoshibiaozhiLWSS': 305, 'gaoshibiaozhiXCTKZDBZ': 306, 'gaoshibiaozhiYJJHJC': 307, 'gaoshibiaozhiYJLRQW': 308, 'lvyouqubiaozhiDJYLQ': 309, 'lvyouqubiaozhiDY': 310, 'lvyouqubiaozhiGEFQ': 311, 'lvyouqubiaozhiHB': 312, 'lvyouqubiaozhiHC': 313, 'lvyouqubiaozhiHX': 314, 'lvyouqubiaozhiQM': 315, 'lvyouqubiaozhiQS': 316, 'lvyouqubiaozhiSD': 317, 'lvyouqubiaozhiTB': 318, 'lvyouqubiaozhiWXC': 319, 'lvyouqubiaozhiYH': 320, 'lvyouqubiaozhiYQFX': 321, 'lvyouqubiaozhiYXC': 322, 'lvyouqubiaozhiYY': 323, 'lvyouqubiaozhiYYD': 324, 'zuoyequDLFB': 325, 'zuoyequQFSG': 326, 'zuoyequXYGD': 327, 'zuoyequXZGD': 328, 'zuoyequYDFB': 329, 'zuoyequZDFB': 330, 'zuoyequZJFB': 331, 'AVP': 332, 'OneCarOneRod': 333, 'PickupPoint': 334, 'DropOffPoint': 335, 'CrossLayerLogo': 336}


def getRSIAlertType(self):
    if(self.param['congested']):
        return RSIAlertType['congested']
    '''
    湿滑/事故...
    if()
    '''
    for k in RSIAlertType.keys():
        if(self.param['owner3D'].Unity_Resource.find(k)>0):
            return RSIAlertType[k]
    return 0


