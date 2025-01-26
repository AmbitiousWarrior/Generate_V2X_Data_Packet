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


MAP_msgCount = 0
def getMAPData():#需要新的地图数据API
    MAPData=MAP.Map_DF()
    try:
        junctions = []
        earth_radius = 6371004     
        print('earth_radius****************',earth_radius)
        RSU_ids= getRsuList()
        for id in RSU_ids:
            junctions.append(getRsuJunction(id))
        Nodes=[]
        print('////',len(junctions),junctions)
        for junction in junctions:
            # if len(junction) <=6 :
            Nodes.append(junction)
            lanes = getIncomingLanes(junction)
        print('Nodes',Nodes) 
        
        global MAP_msgCount
        MAP_msgCount += 1
        if MAP_msgCount>=127:
            MAP_msgCount = MAP_msgCount -127
        MAPData['msgCnt'] = MAP_msgCount    
         
        MAPData['nodes']=[]
        TrafficLightInfo = {}
        for node in Nodes:
            print('111111',node,type(node))
            MapNode=MAP.MapNode_DF()
            MapNode['name']= node
            # MapNode['id']['id']=int(node[-1])
            
            if node.isdigit():
                MapNode['id']['id'] = int(node)%65535
            else:
                MapNode['id']['id'] = 55555
                
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
            MapNode['inLinks']=[]
            
            #在这里组成edges的数据结构
            edges = {}
            edge_names=[]
            edge_names_all=[]
            edge_upstreamNodeIds=[]
            edge_linkWidths=[]
            edge_lanes = []
            edge_points = []
            edge_lanes_points = []     #每一条lane中的points
            edge_Movements = []
            
            lanes = getIncomingLanes(node)
            print('222222',lanes)
        # if len(lanes)>4 :#十字路口  and len(lanes)%4 == 0                
            for v in range(len(lanes)):
                # edge_name = lanes[v][0:lanes[v].rfind('/_')][0:-1]
                edge_name = getEdgeByLane(lanes[v])
                edge_names_all.append(edge_name)
                if edge_name in edge_names:
                    pass
                else:    
                    edge_names.append(edge_name)



            trafficlight_id = getTrafficLightList()     #返回所有交通灯id列表（不含人行横道交通灯）
            print('trafficlight_id',trafficlight_id)
            
            edge_match_trafficlightId = {}
            edge_match_trafficlightId_with_phases = {}
            for id in trafficlight_id:
                trafficlight_type = getTrafficLightType(id)          #返回交通灯类型
                if trafficlight_type == 1:
                    # print('trafficlight_type',trafficlight_type)
                    edge = getTrafficLightEdge(id)              #返回交通灯所作用的edge
                    # print('edge',edge)
                    if edge in edge_names:
                        print('edge222',edge)
                        # trafficlight_phase = getTrafficLightPhase(id)        #返回交通灯相位表
                        # print('trafficlight_phase',trafficlight_phase)
                        edge_match_trafficlightId[edge] = id
                        edge_match_trafficlightId_with_phases[edge] = [id,[0,0,0,0],['0','0','0','0']]

            for i in range(len(edge_match_trafficlightId)):
                list(edge_match_trafficlightId_with_phases.values())[i][1] = [1 + i*4,2 + i*4 ,3 + i*4 ,4 + i*4]
                r_ = getTrafficLightPhase(list(edge_match_trafficlightId_with_phases.values())[i][0], next_junction_direction.right)
                s_ = getTrafficLightPhase(list(edge_match_trafficlightId_with_phases.values())[i][0], next_junction_direction.straight)
                l_ = getTrafficLightPhase(list(edge_match_trafficlightId_with_phases.values())[i][0], next_junction_direction.left)
                u_ = getTrafficLightPhase(list(edge_match_trafficlightId_with_phases.values())[i][0], next_junction_direction.u_turn)
                list(edge_match_trafficlightId_with_phases.values())[i][2] = [r_,s_,l_,u_]
 
            TrafficLightInfo[node] = edge_match_trafficlightId_with_phases
            print('edge_match_trafficlightId',edge_match_trafficlightId)
            print('edge_match_trafficlightId_with_phases',edge_match_trafficlightId_with_phases)


            for i in range(len(edge_names)):  #基于edge开始组包
                MapLink=MAP.MapLink_DF()
                MapLink_name = edge_names[i]
                MapLink['name'] = MapLink_name   # [0:MapLink_name.rfind('/_')][0:-1]
                print('MapLink_name!!!!!!!!!!!!!!!!!',MapLink['name'],type(MapLink_name))
                MapSpeedLimit=MAP.MapSpeedLimit_DF()
                MapSpeedLimit['type']=5
                MapSpeedLimit['speed']=int(16.67/0.02)
                MapLink['speedLimits'].append(MapSpeedLimit)
                
                    
                edge_lanes = getEdgeLanes(edge_names[i])
                Lanes=edge_lanes
                print('333333333333',Lanes,type(Lanes),edge_lanes,type(edge_lanes))
                linkWidth_ = 0
                for lane_ in Lanes:
                    linkWidth_ += getLaneWidth(lane_)
                MapLink['linkWidth']=int(linkWidth_*100)
                    
                    
                MapLink['lanes']=[]
                
                link_upstreamNodeId = getFromJunction(Lanes[-1]) 
                print('link_upstreamNodeId-----------',link_upstreamNodeId,type(link_upstreamNodeId))
                if 'cluster_'  in link_upstreamNodeId:
                    MapLink['upstreamNodeId']['id']=int(link_upstreamNodeId[7:-1].split('_')[1])
                else:
                    # array_ = [int(s) for s in link_upstreamNodeId.split() if s.isdigit()] 
                    array =[]
                    array_ =[]                   
                    for item in link_upstreamNodeId:
                        array.append(item)
                    for s in array:
                        if s.isdigit():
                            array_.append(int(s))
                    print('array_',array_,link_upstreamNodeId.split())
                    lastdigit = array_.pop() 
                    MapLink['upstreamNodeId']['id']=lastdigit  #int(link_upstreamNodeId[-1])
                MapLink['upstreamNodeId']['id'] = int(MapLink['upstreamNodeId']['id']%65535)
                print('44444444444444',link_upstreamNodeId,MapLink['upstreamNodeId']['id']) 
                
                link_points = []               
                for lane_ in Lanes:
                    laneShape_ = getLaneShape(lane_)
                    if len(laneShape_)>28: #剔除掉过多的道路形状点
                        laneShape_step = []
                        step = int(len(laneShape_)/10)
                        laneShape_step.append(laneShape_[0])
                        for n in range(10):  #points 的数量范围 2~31 考虑到包的大小,取12个点
                            laneShape_step.append(laneShape_[1+ step*n])
                        laneShape_step.append(laneShape_[-1])
                        link_points.append(laneShape_step)
                    else:
                        link_points.append(laneShape_)
                
                edgePoints_ = []        
                for ik in range(len(link_points[0])):   #将各lane的形状点集处理成edge的形状点集
                    temp_point_x = 0
                    temp_point_y = 0
                    for j in range(len(Lanes)):  
                        temp_point_x += link_points[j][ik][0]
                        temp_point_y += link_points[j][ik][1]                       
                    edgePoints_.append((temp_point_x/len(Lanes),temp_point_y/len(Lanes)))   
                # print('777777777777777-+-------------------------------++',link_points,len(link_points),edgePoints_)        
                for point in edgePoints_:
                    MapPoint=MAP.MapPoint_DF()
                    lat = (point[1]) * 180.0 / (math.pi * earth_radius) + 39.5427
                    longi = ((point[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                    MapPoint['posOffset']['offsetLL']=('position-LatLon', {'lon':int(10000000*longi), 'lat':int(10000000*lat)})
                    MapLink['points'].append(MapPoint)
                
                for j in range(len(Lanes)):#去掉非机动车道(判断依据, 车道宽度小于3.0m)
                    # print('333333',Lanes[j],type(Lanes[j]))
                    laneWidth = getLaneWidth(Lanes[j])
                    # if laneWidth<3.0: 
                    #     continue
                        
                    MapLane=MAP.MapLane_DF()
                    MapLane['laneID']= i*10+j #int(Lanes[j][-1]) + int(Lanes[j][0])*10
                    print('+++++++++',MapLane['laneID'], Lanes[j],type(Lanes[j]))
                    MapSpeedLimit=MAP.MapSpeedLimit_DF()
                    MapSpeedLimit['type']=5 #'vehicleMaxSpeed'
                    MapSpeedLimit['speed']=int(16.67/0.02)
                    MapLane['speedLimits'].append(MapSpeedLimit)
                    
                    laneShape_ = getLaneShape(Lanes[j])
                    lane_points = []
                    if len(laneShape_)>28: #剔除掉过多的道路形状点
                        laneShape_step = []
                        step = int(len(laneShape_)/10)
                        laneShape_step.append(laneShape_[0])
                        for n in range(10):  #points 的数量范围 2~31 考虑到包的大小,取12个点
                            laneShape_step.append(laneShape_[1+ step*n])
                        laneShape_step.append(laneShape_[-1])
                        lane_points = laneShape_step
                    else:
                        lane_points = laneShape_
                    for point in lane_points: 
                        MapPoint=MAP.MapPoint_DF()
                        lat = (point[1]) * 180.0 / (math.pi * earth_radius) + 39.5427
                        longi = ((point[0]) * 180.0 / (math.pi * earth_radius)) / math.cos(lat * math.pi / 180.0) + (116.2317)
                        MapPoint['posOffset']['offsetLL']=('position-LatLon', {'lon':int(10000000*longi), 'lat':int(10000000*lat)})
                        MapLane['points'].append(MapPoint)

                    connections= getValidDirections(Lanes[j])
                    print('777777777777777',connections)

                    edgebylane = getEdgeByLane(Lanes[j])
                    print('lanebyedge',edgebylane)

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
                        if item==next_junction_direction.u_turn: 
                            AllowedManeuvers[3] = 1
                    maneuvers=[0,0]
                    maneuvers[0]=128*AllowedManeuvers[0]+64*AllowedManeuvers[1]+32*AllowedManeuvers[2]+16*AllowedManeuvers[3]+8*AllowedManeuvers[4]+4*AllowedManeuvers[5]+2*AllowedManeuvers[6]+AllowedManeuvers[7]
                    maneuvers[1]=128*AllowedManeuvers[8]
                    MapLane['maneuvers'][0]=(maneuvers[0], MapLane['maneuvers'][0][1])
                    
                    # PhaseID规则:以edge的数字大小排序，每个edge对应4个phase（1-16）

                    for k in range(len(connections)): #:开头的是junction的内部lane，不可以用内部lane调用getToJunction函数                        
                        MapConnection=MAP.MapConnection_DF()
                        toLanes=getNextLanes(Lanes[j], connections[k])
                        tolane = []
                        for item in toLanes:
                            if item[0] != ':':
                                tolane.append(item)
                        MapConnection['connectingLane']['lane']= int(tolane[0][-1]) + int(tolane[0][-3])*10 
                        
                        
                        #---------------------20230704 添加填写MapConnection['connectingLane']['maneuvers']字段
                        AllowedManeuvers2 = [0,0,0,0,0,0,0,0,0]
                        if connections[k]==next_junction_direction.straight:
                            AllowedManeuvers2[0] = 1
                        if connections[k]==next_junction_direction.left:   
                            AllowedManeuvers2[1] = 1
                        if connections[k]==next_junction_direction.right: 
                            AllowedManeuvers2[2] = 1
                        # if item==next_junction_direction.uturn: 
                        #     AllowedManeuvers[3] = 1
                        maneuvers2=[0,0]
                        maneuvers2[0]=128*AllowedManeuvers2[0]+64*AllowedManeuvers2[1]+32*AllowedManeuvers2[2]+16*AllowedManeuvers2[3]+8*AllowedManeuvers2[4]+4*AllowedManeuvers2[5]+2*AllowedManeuvers2[6]+AllowedManeuvers2[7]
                        maneuvers2[1]=128*AllowedManeuvers2[8]
                        # MapLane['maneuvers'][0]=(maneuvers2[0], MapLane['maneuvers'][0][1])
                        MapConnection['connectingLane']['maneuver'][0] = (maneuvers2[0], 0)
                        print('++++++++++++++++++++++++++++++++++++++++++++++MapLane_connectingLane_maneuver',MapConnection['connectingLane']['maneuver'])
                        #---------------------20230704 
                        
                        
                        
                        print('****',tolane,getToJunction(tolane[0]))
                        print('****',getToJunction(tolane[0])[7:-1])
                        print('****',getToJunction(tolane[0])[8:-1].split('_')[0])
                        if '_' in getToJunction(tolane[0]):
                            MapConnection['remoteIntersection']['id']=  int(getToJunction(tolane[0])[8:-1].split('_')[0].translate({ ord("0"): None })) 
                        else:
                            MapConnection['remoteIntersection']['id']=  int(getToJunction(tolane[0])[-1]) # int(getToJunction(tolane[0]).translate({ ord("0"): None }))  
                        print('88888888888888888888',toLanes,tolane,getToJunction(tolane[0]),MapConnection['remoteIntersection']['id'])
                        if edgebylane in edge_match_trafficlightId_with_phases.keys():
                            if connections[k]==next_junction_direction.right:
                                MapConnection['phaseId']= edge_match_trafficlightId_with_phases[edgebylane][1][0]
                            if connections[k]==next_junction_direction.straight:
                                MapConnection['phaseId']= edge_match_trafficlightId_with_phases[edgebylane][1][1]
                            if connections[k]==next_junction_direction.left:
                                MapConnection['phaseId']= edge_match_trafficlightId_with_phases[edgebylane][1][2] 
                            if connections[k]==next_junction_direction.u_turn:
                                MapConnection['phaseId']= edge_match_trafficlightId_with_phases[edgebylane][1][3]
                            print('phaseId2999999999999999999999999999999999999999999999999999999999999999999',MapConnection['phaseId'])
                        else:
                            MapConnection['phaseId']= 0
                                                        
                        MapLane['connectsTo'].append(MapConnection)
 
                        if len(MapLane['connectsTo'])== 0:  
                                MapLane.pop('connectsTo')
                                    
    
                    MapLink['lanes'].append(MapLane)    
                MapNode['inLinks'].append(MapLink)
            MAPData['nodes'].append(MapNode)



            # tempdirt_for_remoteIntersection_id = [[],[],[],[]]
            # tempdirt_for_remoteIntersection_phaseId = [[],[],[],[]]
            tempdirt_for_remoteIntersection_id = [list() for i in range(len(MapNode['inLinks']))]
            tempdirt_for_remoteIntersection_phaseId = [list() for i in range(len(MapNode['inLinks']))]
            print('55555555555555',tempdirt_for_remoteIntersection_id)
            print('--------------',tempdirt_for_remoteIntersection_phaseId)
            #组成link movement字段
            for i in range(len(MapNode['inLinks'])):
                for item in MapNode['inLinks'][i]['lanes']:
                    if len(item['connectsTo'])>0:
                        for item_connectsTO in item['connectsTo']:
                            tempdirt_for_remoteIntersection_id[i].append(item_connectsTO['remoteIntersection']['id'])   
                            tempdirt_for_remoteIntersection_phaseId[i].append(item_connectsTO['phaseId'])                           
            print('55555555555555',tempdirt_for_remoteIntersection_id)
            print('--------------',tempdirt_for_remoteIntersection_phaseId)
                

            for i in range(len(MapNode['inLinks'])):    
                edge_directions_num = len(tempdirt_for_remoteIntersection_id[i])#一条edge中所有lane的可连接方向总数
                edge_phaseId_num = len(tempdirt_for_remoteIntersection_phaseId[i])
                print('9999999',edge_directions_num, edge_phaseId_num) 
                list_movement = sorted(set(tempdirt_for_remoteIntersection_id[i]),key=tempdirt_for_remoteIntersection_id[i].index) #去除重复的remoteIntersection，顺序保持不变
                list_phaseId = sorted(set(tempdirt_for_remoteIntersection_phaseId[i]),key=tempdirt_for_remoteIntersection_phaseId[i].index)                    
                print('999999999999999999999',list_movement,list_phaseId)
                
                for k in range(len(list_movement)):                       
                    MapMovement=MAP.MapMovement_DF()
                    MapMovement['remoteIntersection']={}
                    MapMovement['remoteIntersection']['region']=1
                    MapMovement['remoteIntersection']['id']=list_movement[k]
                    if len(list_movement) == len(list_phaseId): #如果两者长度一致，则一一对应
                        MapMovement['phaseId']=list_phaseId[k]
                    else:
                        if k == len(list_movement)-1:#这里的逻辑是：把左转的交通灯相位赋值为list_phaseId中的最后一个（因为list_movement是按顺序r s l 生成的），其余的均为右转和直行的情况
                            MapMovement['phaseId']=list_phaseId[-1]
                        else:
                            MapMovement['phaseId']=list_phaseId[0]
                    MapNode['inLinks'][i]['movements'].append(MapMovement)


    except Exception as ex:
        print(ex)
        print(ex.__traceback__.tb_lineno) 
        return MAPData
    else:
        dataOutputPath0 = getDataOutputPath()
        dataOutputPath = str.replace(dataOutputPath0,'/','\\')
        database_path1 = os.path.split(os.path.realpath(__file__))[0]
        database_path2 = 'PanoSimDatabase'
        database_path = database_path1[:database_path1.index(database_path2)]

        path_share = os.path.join(os.path.expanduser('~'),"Desktop")
        print('Path_MAP_file',database_path + 'PanoSimDatabase\Experiment\\' + dataOutputPath + '\MAP_message_Test.txt')
        with open(database_path + 'PanoSimDatabase\Experiment\\' + dataOutputPath + '\MAP_message_Test.txt', 'w') as output_file:
            output_file.write(str(MAPData))
        with open(database_path + 'PanoSimDatabase\Experiment\\' + dataOutputPath + '\SPAT_message_Test.txt', 'w') as output_file:
            output_file.write(str(TrafficLightInfo))
        return MAPData, TrafficLightInfo


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
