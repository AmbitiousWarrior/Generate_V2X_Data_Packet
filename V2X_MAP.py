#  场景描述：step1触发发车模型，创建自己的接口车作为V2X场景中的RV；
#           step2基于obud的车控指令控制车辆的驾驶行为：纵向距离、横向默认具体为车道线宽度左右方向根据发车lane决定、发车速度、车辆类型、触发车道

import math
from xml.dom.minidom import parseString
import numpy as np
import sys
import json
# import dicttoxml
import random
# import const
import mmap
import time
from TrafficModelInterface import *
import os
#获取文件父目录
V2X_MAP_Dir = os.path.dirname(__file__)
print('V2X_MAP_Dir',V2X_MAP_Dir,os.path.join(os.path.expanduser('~'),"Desktop"))
import MAP

def getMAPData():#需要新的地图数据API
    MAPData=MAP.Map_DF()
    try:
        earth_radius = 6371004     

        junctions = getJunctionList()
        Nodes=[]
        print('////',len(junctions),junctions)
        for junction in junctions:
            # print(len(junction))
            if len(junction)<=6:#剔除internal junction(内部junction都比较长？TOTEST)
                # print(junction)
                Nodes.append(junction)
            lanes = getIncomingLanes(junction)
            # print('**********',junction)
            # print('----------',len(lanes))
            # print('-----------------------------------')
            # print(lanes)
            # print('-----------------------------------')
        print('Nodes',Nodes)      
        MAPData['nodes']=[]
        for node in Nodes:
            print('111111',node,type(node))
            MapNode=MAP.MapNode_DF()
            MapNode['name']= node
            MapNode['id']['id']=int(node[-1])  #0
            MapNode['refPos']={}
            #refPos
            node_shape = getJunctionShape(node)
            total_x = 0.0
            total_y = 0.0
            for item in node_shape:
                total_x = total_x+item[0]
                total_y = total_y+item[1]
            avg_x = total_x/len(node_shape)
            avg_y = total_y/len(node_shape)
            lat = (avg_y) * 180.0 / (math.pi * earth_radius) + 39.5427
            longi = ((avg_x) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
            MapNode['refPos']['lat']=int(10000000 * lat)
            MapNode['refPos']['long']=int(10000000 * longi)
            MapNode['refPos']['elevation']=0
            # MAPData['nodes'].append(MapNode) #这个要写在最后面
            MapNode['inLinks']=[]
            
            #在这里组成edges的数据结构
            edges = {}
            edge_names=[]
            edge_upstreamNodeIds=[]
            edge_speedLimits=[]
            edge_linkWidths=[]
            edge_lanes = []
            edge_points = []
            edge_Movements = []
            
            lanes = getIncomingLanes(node)
            print('222222',lanes)
            if len(lanes)>4 and len(lanes)%4 == 0:#十字路口
                edge_num = int(len(lanes)/4)
                for i in range(4):
                    if lanes[i*edge_num].startswith('-'):                    
                        edge_name = lanes[i*edge_num][0:8]
                    else:
                        edge_name = lanes[i*edge_num][0:6]
                    edge_names.append(edge_name)
                    edge_upstreamNodeIds.append(getFromJunction(lanes[i*edge_num]))
                    edge_speedLimits.append(16.67)
                    edge_linkWidths.append(3.5*edge_num)
                    edgeLanes = []
                    remotejunctions = []
                    for j in range(edge_num):
                        edgeLanes.append(lanes[i*edge_num+j])
                        # print('333333',lanes[i*edge_num+j],type(lanes[i*edge_num+j]))
                        laneShape = getLaneShape(lanes[i*edge_num+j])
                        edgePoints = np.array([0.0 for x in range(0,len(laneShape))]) + np.array(laneShape) 
                        
                        directions = getValidDirections(lanes[i*edge_num+j])
                        for direction in directions:                          
                            nextlanes = getNextLanes(lanes[i*edge_num+j], direction)
                            nextlane = []
                            for lane in nextlanes:
                                if lane.startswith(':'): 
                                    pass
                                else :
                                    nextlane.append(lane)
                            remotejunction = getToJunction(nextlane[0])
                            remotejunctions.append(remotejunction)
                    
                    edge_lanes.append(edgeLanes)
                    edge_points.append(edgePoints)
                    edge_Movements.append(remotejunctions)
                        
            elif isDeadEnd(lanes[0]):  #判断是否有lane为死路
                if lanes[0].startswith('-'):                 
                    edge_name = lanes[0][0:7]
                else:
                    edge_name = lanes[0][0:6]  
                edge_names.append(edge_name)
                edge_upstreamNodeIds.append(getFromJunction(lanes[0]))
                edge_speedLimits.append(0)#16.67
                edge_linkWidths.append(3.5*len(lanes))
                edgeLanes = []
                remotejunctions = []
                for j in range(len(lanes)):
                    edgeLanes.append(lanes[j])
                    laneShape = getLaneShape(lanes[j])
                    edgePoints = np.array([0.0 for x in range(0,len(laneShape))]) + np.array(laneShape) 

                remotejunction = getToJunction(lanes[0])

                edge_lanes.append(edgeLanes)
                edge_points.append(edgePoints)
                edge_Movements.append(remotejunction)
       
            
            for i in range(len(edge_names)):
                MapLink=MAP.MapLink_DF()
                MapLink['name']=edge_names[i]
                MapSpeedLimit=MAP.MapSpeedLimit_DF()
                MapSpeedLimit['type']=5
                MapSpeedLimit['speed']=int((edge_speedLimits[i])/0.02)
                MapLink['speedLimits'].append(MapSpeedLimit)
                for point in edge_points[i]:
                    MapPoint=MAP.MapPoint_DF()
                    lat = (point[1]) * 180.0 / (math.pi * earth_radius) + 39.5427
                    longi = ((point[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                    MapPoint['posOffset']['offsetLL']=('position-LatLon', {'lon':int(10000000*longi), 'lat':int(10000000*lat)})
                    MapLink['points'].append(MapPoint)
                Lanes=edge_lanes[i]
                # print('333333333333',Lanes,type(Lanes),edge_lanes,type(edge_lanes))
                if(len(Lanes) > 0):
                    MapLink['linkWidth']=int(edge_linkWidths[i]*100)
                    MapLink['lanes']=[]
                    # MapLink['upstreamNodeId']['id']=edge_upstreamNodeIds[i]  
                    MapLink['upstreamNodeId']['id']=int(edge_upstreamNodeIds[i][-1])
                    # print('44444444444444',edge_upstreamNodeIds[i],MapLink['upstreamNodeId']['id'])
                
                for j in range(len(Lanes)):#去掉非机动车道(判断依据，车道宽度小于3.0m)
                    # print('333333',Lanes[j],type(Lanes[j]))
                    laneWidth = getLaneWidth(Lanes[j])
                    if laneWidth<3.0: 
                        continue
                        
                    MapLane=MAP.MapLane_DF()
                    MapLane['laneID']= int(Lanes[j][-1]) + int(Lanes[j][-3])*10 #Lanes[j]
                    # print('+++++++++',MapLane['laneID'], Lanes[j],type(Lanes[j]))
                    MapSpeedLimit=MAP.MapSpeedLimit_DF()
                    MapSpeedLimit['type']=5 #'vehicleMaxSpeed'
                    MapSpeedLimit['speed']=int(edge_speedLimits[i]/0.02)
                    MapLane['speedLimits'].append(MapSpeedLimit)
                                      
                    for point in getLaneShape(Lanes[j]): 
                        MapPoint=MAP.MapPoint_DF()
                        lat = (point[1]) * 180.0 / (math.pi * earth_radius) + 39.5427
                        longi = ((point[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                        MapPoint['posOffset']['offsetLL']=('position-LatLon', {'lon':int(10000000*longi), 'lat':int(10000000*lat)})
                        MapLane['points'].append(MapPoint)

                    connections= getValidDirections(Lanes[j])
                    print('777777777777777',connections)
                    direction = []
                    AllowedManeuvers = [0,0,0,0,0,0,0,0,0]
                    for item in connections:
                        direction.append(item)#TOTEST
                    direction = list(set(direction))
                    # print('88888888888888',direction)
                    for item in direction:
                        if item==next_junction_direction.straight:
                            AllowedManeuvers[0] = 1
                        if item==next_junction_direction.left:   
                            AllowedManeuvers[1] = 1
                        if item==next_junction_direction.right: 
                            AllowedManeuvers[2] = 1
                        # if item==next_junction_direction.uturn: 
                        #     AllowedManeuvers[3] = 1
                    maneuvers=[0,0]
                    maneuvers[0]=128*AllowedManeuvers[0]+64*AllowedManeuvers[1]+32*AllowedManeuvers[2]+16*AllowedManeuvers[3]+8*AllowedManeuvers[4]+4*AllowedManeuvers[5]+2*AllowedManeuvers[6]+AllowedManeuvers[7]
                    maneuvers[1]=128*AllowedManeuvers[8]
                    MapLane['maneuvers'][0]=(maneuvers[0], MapLane['maneuvers'][0][1])
                    
                    for k in range(len(connections)): #:开头的是junction的内部lane，不可以用内部lane调用getToJunction函数
                        MapConnection=MAP.MapConnection_DF()
                        toLanes=getNextLanes(Lanes[j], connections[k])
                        tolane = []
                        for item in toLanes:
                            if item[0] != ':':
                                tolane.append(item)
                        # MapConnection['connectingLane']['lane']=tolane[0]
                        MapConnection['connectingLane']['lane']= int(tolane[0][-1]) + int(tolane[0][-3])*10 
                        MapConnection['remoteIntersection']['id']=int(getToJunction(tolane[0])[-1])
                        print('88888888888888888888',toLanes,tolane[0],toLanes[0],getToJunction(tolane[0]))
                        if i == 0:#0表示自北向南的第一个edge，其直行和右转使用4相位交通灯的第三相位，左转使用第四相位
                            if connections[k]==next_junction_direction.straight or connections[k]==next_junction_direction.right:
                                MapConnection['phaseId']= 3
                            if connections[k]==next_junction_direction.left:
                                MapConnection['phaseId']= 4
                        if i == 1:#1表示自东向西的第二个edge，其直行和右转使用4相位交通灯的第一相位，左转使用第二相位
                            if connections[k]==next_junction_direction.straight or connections[k]==next_junction_direction.right:
                                MapConnection['phaseId']= 1
                            if connections[k]==next_junction_direction.left:
                                MapConnection['phaseId']= 2                        
                        if i == 2:#2表示自南向北的第三个edge，其直行和右转使用4相位交通灯的第三相位，左转使用第四相位
                            if connections[k]==next_junction_direction.straight or connections[k]==next_junction_direction.right:
                                MapConnection['phaseId']= 3
                            if connections[k]==next_junction_direction.left:
                                MapConnection['phaseId']= 4                        
                        if i == 3:#3表示自西向东的第四个edge，其直行和右转使用4相位交通灯的第一相位，左转使用第二相位
                            if connections[k]==next_junction_direction.straight or connections[k]==next_junction_direction.right:
                                MapConnection['phaseId']= 1
                            if connections[k]==next_junction_direction.left:
                                MapConnection['phaseId']= 2
                        MapLane['connectsTo'].append(MapConnection)
 
                        if len(MapLane['connectsTo'])== 0:  
                                MapLane.pop('connectsTo')
                                    
    
                    MapLink['lanes'].append(MapLane)    
                MapNode['inLinks'].append(MapLink)
            MAPData['nodes'].append(MapNode)

            #[5, 4, 4, 4, 3, 2, 5, 5, 5, 4, 3, 2, 2, 2, 5, 4, 3, 3, 3, 2]十字路口各link(正北开始的顺时针方向 北东南西)的各lane连接的remoteIntersection(crossroads地图， right straight.straight.straight left)
            
            tempdirt_for_remoteIntersection_id = []
            tempdirt_for_remoteIntersection_phaseId = []
            if len(MapNode['inLinks'])>=4:
                for i in range(len(MapNode['inLinks'])):
                    for item in MapNode['inLinks'][i]['lanes']:
                        if len(item['connectsTo'])>0:
                            for item_connectsTO in item['connectsTo']:
                                tempdirt_for_remoteIntersection_id.append(item_connectsTO['remoteIntersection']['id'])   
                                tempdirt_for_remoteIntersection_phaseId.append(item_connectsTO['phaseId'])                                
                print('55555555555555',tempdirt_for_remoteIntersection_id)
                print('--------------',tempdirt_for_remoteIntersection_phaseId)
                
            if len(MapNode['inLinks'])==4:
                for i in range(len(MapNode['inLinks'])):    
                    edge_directions_num = int(len(tempdirt_for_remoteIntersection_id)/4) #一条edge中所有lane的可连接方向总数
                    edge_phaseId_num = int(len(tempdirt_for_remoteIntersection_phaseId)/4)
                    print('9999999',edge_directions_num, edge_phaseId_num)
                    edge_directions = tempdirt_for_remoteIntersection_id[0+edge_directions_num*i:edge_directions_num+edge_directions_num*i]      
                    edge_phaseIds = tempdirt_for_remoteIntersection_phaseId[0+edge_phaseId_num*i:edge_phaseId_num+edge_phaseId_num*i]    
                    list_movement = sorted(set(edge_directions),key=edge_directions.index) #去除重复的remoteIntersection，顺序保持不变
                    list_phaseId = sorted(set(edge_phaseIds),key=edge_phaseIds.index)                    
                    print('999999999999999999999',list_movement,list_phaseId)
                    
                    for k in range(len(list_movement)):                       
                        MapMovement=MAP.MapMovement_DF()
                        MapMovement['remoteIntersection']={}
                        MapMovement['remoteIntersection']['region']=0
                        MapMovement['remoteIntersection']['id']=list_movement[k]
                        if k == len(list_movement)-1:#这里的逻辑是：把左转的交通灯相位赋值为list_phaseId中的最后一个（因为list_movement是按顺序r s l 生成的），其余的均为右转和直行的情况
                            MapMovement['phaseId']=list_phaseId[-1]
                        else:
                            MapMovement['phaseId']=list_phaseId[0]
                        MapNode['inLinks'][i]['movements'].append(MapMovement)
                
                        
        # if len(MAPData['nodes']) >= 10:  
        #     for i in range(len(MAPData['nodes'])):   
        #         for j in range(len(MAPData['nodes'][i]['inLinks'])): 
        #             MAPData['nodes'][i]['inLinks'][j].pop('movements')

    except Exception as ex:
        print(ex)
        return MAPData
    else:
        path_share = os.path.join(os.path.expanduser('~'),"Desktop")
        with open(path_share + 'MAP_message_szdx.txt', 'w') as output_file:
            output_file.write(str(MAPData))
            output_file.close()
            print('1111111111111111111111111111111111111111111111111111111111111')
        return MAPData


def ModelStart(userData):
    #初始化将参数全部传递给UserData，output中进行逻辑判断选择赋值
    userData["phase"] = 0
    userData["judge"] = 0
    Global_in = userData['parameters'] #UI的输入
    print('开始组包...')
    getMAPData()


def ModelOutput(userData, true=1):

    pass

def ModelTerminate(userData):
    pass
