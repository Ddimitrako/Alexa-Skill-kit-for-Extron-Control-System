## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import ProcessorDevice, UIDevice
from extronlib.interface import EthernetClientInterface, \
    EthernetServerInterface, SerialInterface, IRInterface, RelayInterface, \
    ContactInterface, DigitalIOInterface, FlexIOInterface, SWPowerInterface, \
    VolumeInterface
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait,Timer
from extronlib.interface import EthernetServerInterfaceEx
from Video_Switching import Preset_Buttons,SecondBtnList,Update_Matrix
from ON_OFF import LightButtonHandler,Projector_Power_ON,Projector_Power_OFF,System_ON,System_OFF
from ON_OFF import Projector_ON,Projector_OFF,AllOn,AllOff,LightingSystem
import re
import json
from Audio_Control import Set_Volume,Level_Mute_Unmute,Tesira

serv = EthernetServerInterfaceEx(4001, 'TCP')
serv.StartListen()    
if serv.StartListen() != 'Listening':
     print('Port unavailable: check firewall / port number')


AlexaFeedback={
'System_ON':'on',
'System_OFF':'off',

'Projector_ON':'Monitors on',
'Projector_OFF':'Monitors off',

'AllShadesStop':'Shades: stop',
'AllShadesUp':'Shades: on',
'AllShadesDown':'Shades: off',

'AllOn':'Lights: on',
'AllOff':'Lights: off',
'WarmLights':'Lights: warm',
'ColdLights':'Lights: cold',

'Preset'    :'Preset:',
'PC'        :'Preset: PC',
'ClickShare':'Preset: click',
'HDMI'     :'Preset: HDMI',
'TV'        :'Preset: TV',
'Cisco'    :'Preset: Cisco',

'Matrix'    :'Matrix:',
'PC'        :'PC',
'ClickShare':'click',
'HDMI'      :'HDMI',
'TV'        :'TV',
'Cisco'     :'Cisco',
}

AlexaSynonims={
'leftSynonim':['left','one','1'],
'rightSynonim':['right','two','2','second','write'],
'bothSynonim':['both','one and two','1 and 2','right and left'],
}

VolumeMode=['mute','unmute','max','min']
            
                
"""*****************MAtrix*********************"""               
@event(serv, 'ReceiveData')
def HandleReceiveMatrix(client, data):
    print(data)    
    data=data.decode('UTF-8')  
    if 'Lights: on' in data:
        LightingSystem.Set('RelayControl','On', {'Address':103}) #103=allon
        LightingSystem.Set('RelayControl','Off', {'Address':109}) #front face off
    elif 'Lights: off' in data:               
        LightingSystem.Set('RelayControl','Off', {'Address':103}) 
    elif 'Monitors on' in data:
        Projector_Power_ON()
    elif 'Monitors off' in data:
        Projector_Power_OFF()            
    elif 'Shades: stop' in data:
        LightingSystem.Set('RelayControl','On', {'Address':302}) 
        LightingSystem.Set('RelayControl','On', {'Address':303}) 
    elif 'Shades: on' in data:
        LightingSystem.Set('RelayControl','Off', {'Address':301}) 
        LightingSystem.Set('RelayControl','Off', {'Address':300}) 
    elif 'Shades: off' in data:
        LightingSystem.Set('RelayControl','On', {'Address':300})    
        LightingSystem.Set('RelayControl','On', {'Address':301}) 
        
    if 'Volume:' in data:        
        if ' mute' in data:
            Level_Mute_Unmute(True)
            print('Volume mute Done')
        elif 'unmute' in data:
            Level_Mute_Unmute(False)
            print('Volume unmute Done')
        elif 'max' in data:
            Set_Volume(0)
            print('Volume max Done')
        elif 'Min' in data:             
            Set_Volume(-50)
            print('Volume Min Done')
        else:
            matchVolumeValue = re.findall(r'[0-9]+', data)
            print(matchVolumeValue)
            #Set_Volume(int(matchVolumeValue[0]/2)-50)
            Volume=int(matchVolumeValue[0])/2-50
            Tesira.Set('LevelControl', Volume, {'Instance Tag': 'Level7', 'Channel': '1'})


    if 'Preset:' in data:
        if 'clickshare' in data:
            Preset_Buttons(SecondBtnList[0],"Pressed") 
            print('Preset Clicshare selected ')            
        elif 'Cisco' in data:
            Preset_Buttons(SecondBtnList[2],"Pressed")  
            print('Preset Cisco selected ')  
        elif 'PC' in data:
            Preset_Buttons(SecondBtnList[4],"Pressed") 
            print('Preset PC selected ')             
        elif 'HDMI' in data:
            Preset_Buttons(SecondBtnList[5],"Pressed") 
            print('Preset HDMI selected ') 
            
            
    if 'Matrix:' in data:
        if 'PC' in data:        
            for key, lista in AlexaSynonims.items():            
                for synonim in lista:
                    if synonim in data:
                        if key=='leftSynonim':
                            Update_Matrix(1,1)
                            print("pc left screen done")
                        elif key=='rightSynonim':
                            Update_Matrix(1,2)
                            print("pc right screen done")
                        elif key=='bothSynonim':
                            Update_Matrix(1,1)
                            Update_Matrix(6,2)
                            print("pc both screens done")                
        if 'click' in data:        
            for key, lista in AlexaSynonims.items():            
                for synonim in lista:
                    if synonim in data:
                        if key=='leftSynonim':
                            Update_Matrix(4,1)
                            print("clickshare left screen done")
                        elif key=='rightSynonim':
                            Update_Matrix(4,2)
                            print("clickshare right screen done")
                        elif key=='bothSynonim':
                            Update_Matrix(4,1)
                            Update_Matrix(4,2)
                            print("clickshare both screens done")                 
        if 'Hdmi' in data:        
            for key, lista in AlexaSynonims.items():            
                for synonim in lista:
                    if synonim in data:
                        if key=='leftSynonim':
                            Update_Matrix(2,1)
                            print("Hdmi left screen done")
                        elif key=='rightSynonim':
                            Update_Matrix(2,2)
                            print("Hdmi right screen done")
                        elif key=='bothSynonim':
                            Update_Matrix(2,1)
                            Update_Matrix(2,2)
                            print("Hdmi both screens done")            
        if 'cisco' in data:        
            for key, lista in AlexaSynonims.items():            
                for synonim in lista:
                    if synonim in data:
                        if key=='leftSynonim':
                            Update_Matrix(2,1)
                            print("cisco left screen done")
                        elif key=='rightSynonim':
                            Update_Matrix(2,2)
                            print("cisco right screen done")
                        elif key=='bothSynonim':
                            Update_Matrix(2,1)
                            Update_Matrix(2,2)
                            print("cisco both screens done")                    
        

    
   