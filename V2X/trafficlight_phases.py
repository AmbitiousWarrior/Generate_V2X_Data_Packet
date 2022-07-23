from V2X.Message  import *


def creat_intersection_phases(now_time):
    now_time = now_time-now_time%10
    intersection=SPAT.SPATIntersectionState_DF()
    intersection['intersectionId']['id'] = 0            
    if 0<=now_time<300:        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 5
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(300-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(300-now_time)
        counting['likelyEndTime']=int(330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(330-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(330-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(330-now_time)
        counting['likelyEndTime']=int(610-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(610-now_time)
        counting['likelyEndTime']=int(640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(640-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(640-now_time)
        counting['likelyEndTime']=int(1040-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1040-now_time)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070-now_time)
        counting['likelyEndTime']=int(1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        # return intersection['phases']
        return intersection
    
    
    if 300<=now_time<330:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 8
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(30+300-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(30+300-now_time)
        counting['likelyEndTime']=int(1070+300-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070+300-now_time)
        counting['likelyEndTime']=int(1370+300-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(330-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(330-now_time)
        counting['likelyEndTime']=int(610-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(610-now_time)
        counting['likelyEndTime']=int(640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(640-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(640-now_time)
        counting['likelyEndTime']=int(1040-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1040-now_time)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070-now_time)
        counting['likelyEndTime']=int(1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    if 330<=now_time<610:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1040+330-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1040+330-now_time)
        counting['likelyEndTime']=int(1340+330-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 5
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(280+330-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(280+330-now_time)
        counting['likelyEndTime']=int(310+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(310+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(640-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(640-now_time)
        counting['likelyEndTime']=int(1040-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1040-now_time)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070-now_time)
        counting['likelyEndTime']=int(1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    if 610<=now_time<640:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1040+330-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1040+330-now_time)
        counting['likelyEndTime']=int(1340+330-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 8
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(30+610-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(30+610-now_time)
        counting['likelyEndTime']=int(1090+610-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1090+610-now_time)
        counting['likelyEndTime']=int(1370+610-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(640-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(640-now_time)
        counting['likelyEndTime']=int(1040-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1040-now_time)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070-now_time)
        counting['likelyEndTime']=int(1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    if 640<=now_time<1040:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1040+330-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1040+330-now_time)
        counting['likelyEndTime']=int(1340+330-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1060+640-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1060+640-now_time)
        counting['likelyEndTime']=int(1340+640-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+640-now_time)
        counting['likelyEndTime']=int(1370+640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 5
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(400+640-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(400+640-now_time)
        counting['likelyEndTime']=int(430+640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(430+640-now_time)
        counting['likelyEndTime']=int(1370+640-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070-now_time)
        counting['likelyEndTime']=int(1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    if 1040<=now_time<1070:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1040+330-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1040+330-now_time)
        counting['likelyEndTime']=int(1340+330-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1060+640-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1060+640-now_time)
        counting['likelyEndTime']=int(1340+640-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+640-now_time)
        counting['likelyEndTime']=int(1370+640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 8
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(30+1040-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(30+1040-now_time)
        counting['likelyEndTime']=int(970+1040-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(970+1040-now_time)
        counting['likelyEndTime']=int(1370+1040-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1070-now_time)
        counting['likelyEndTime']=int(1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340-now_time)
        counting['likelyEndTime']=int(1370-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    if 1070<=now_time<1340:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1040+330-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1040+330-now_time)
        counting['likelyEndTime']=int(1340+330-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1060+640-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1060+640-now_time)
        counting['likelyEndTime']=int(1340+640-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+640-now_time)
        counting['likelyEndTime']=int(1370+640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(940+1070-now_time)
        counting['nextDuration']=940
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(940+1070-now_time)
        counting['likelyEndTime']=int(1340+1070-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+1070-now_time)
        counting['likelyEndTime']=int(1370+1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 5
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(270+1070-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(270+1070-now_time)
        counting['likelyEndTime']=int(300+1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(300+1070-now_time)
        counting['likelyEndTime']=int(1370+1070-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    
    if 1340<=now_time<1370:
        phases=SPAT.SPATPhase_DF()           
        phases['id']=1     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1040+330-now_time)
        counting['nextDuration']=1040
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1040+330-now_time)
        counting['likelyEndTime']=int(1340+330-now_time)
        counting['nextDuration']=300
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+330-now_time)
        counting['likelyEndTime']=int(1370+330-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 


        phases=SPAT.SPATPhase_DF()           
        phases['id']=2     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(1060+640-now_time)
        counting['nextDuration']=1060
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1060+640-now_time)
        counting['likelyEndTime']=int(1340+640-now_time)
        counting['nextDuration']=280
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+640-now_time)
        counting['likelyEndTime']=int(1370+640-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=3     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 3
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(940+1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(940+1070-now_time)
        counting['likelyEndTime']=int(1340+1070-now_time)
        counting['nextDuration']=400
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 8
        counting={}
        counting['startTime']=int(1340+1070-now_time)
        counting['likelyEndTime']=int(1370+1070-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        
        
        phases=SPAT.SPATPhase_DF()           
        phases['id']=4     
        
        phase=SPAT.SPATPhaseState_DF()             
        phase['light'] = 8
        counting={}
        counting['startTime']=int(0)
        counting['likelyEndTime']=int(30+1340-now_time)
        counting['nextDuration']=30
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseState_DF()
        phase['light'] = 3
        counting={}
        counting['startTime']=int(30+1340-now_time)
        counting['likelyEndTime']=int(1100+1340-now_time)
        counting['nextDuration']=1070
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        phase=SPAT.SPATPhaseStae_DF()
        phase['light'] = 5
        counting={}
        counting['startTime']=int(1100+1340-now_time)
        counting['likelyEndTime']=int(1370+1340-now_time)
        counting['nextDuration']=270
        phase['timing']=('counting', counting)
        phases['phaseStates'].append(phase)
        
        intersection['phases'].append(phases) 
        return intersection
    
    
    
#抽象的话，抓住相位变化，写循化比较好（不同时间段之间，变的只有1或2个相位）