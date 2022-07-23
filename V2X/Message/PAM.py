def VIR_DF():
    df = {}

    df['msgCnt'] = 0
    #df['id'] = b'00000000'
    df['id'] = '00000000'

    df['secMark'] = 0

    df['pos'] = {}
    #pos
    df['pos']['lat'] = 0
    df['pos']['long'] = 0
    df['pos']['elevation'] = 0 #optioinal

  
    df['pathPlanning'] = {}
    #pathPlanning
    df['pathPlanning']['x'] = []
    df['pathPlanning']['y'] = []
    df['pathPlanning']['z'] = [] #'unavailable' optioinal 
    df['pathPlanning']['t'] = [] 
    df['pathPlanning']['v'] = [] 
    df['pathPlanning']['a'] = [] 

    df['reqs'] = {}
    #reqs
    df['reqs']['changeLaneToLeft'] = 0 # 不知如何定义请求，字段？？？？？
    df['reqs']['changeLaneToRight'] = 1
    df['reqs']['acceleration'] = 2
    df['reqs']['deceleration'] = 3
    df['reqs']['speedKeeping'] = 4


    df['currentBehavior'] = {} #optioinal
    #motionCfd
    df['currentBehavior']['？？？？？'] = 0  #'unavailable' optioinal


    return df

def PrepareForCode(vir):
    import copy
    codetobe=copy.deepcopy(vir)
    
    codetobe['id']=str.encode(vir['id'])
    if(len(codetobe['id'])>8):
        codetobe['id']=codetobe['id'][0:7]
    else:
        while(len(codetobe['id'])<8):
            codetobe['id']=codetobe['id']+b'\x00'

    codetobe['secMark']=round(vir['secMark']*1000)

    codetobe['pos']['lat']=round(vir['pos']['lat'])
    codetobe['pos']['long']=round(vir['pos']['long'])
    codetobe['pos']['elevation']=round(vir['pos']['elevation'])



    return codetobe

    
if __name__=='__main__':

    import os
    import asn1tools

    dir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    asnPath=dir+'\\asn\\LTEV.asn'
    ltevCoder=asn1tools.compile_files(asnPath, 'uper', numeric_enums=True)

    import json
    bsmPath=dir+'\\bsm.json'  #???????????来自哪
    bsmData=json.load(open(bsmPath,'r'))
    #bsmData=BSM_DF()

    bsmEncoded=ltevCoder.encode('BasicSafetyMessage', PrepareForCode(bsmData))
    print(bsmEncoded)
    bsmDecoded=ltevCoder.decode('BasicSafetyMessage', bsmEncoded)
    print('finish')