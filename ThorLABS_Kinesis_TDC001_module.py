# from https://github.com/Thorlabs/Motion_Control_Examples/blob/main/Python/KCube/KDC101/kdc101_pythonnet.py
"""An example that uses the .NET Kinesis Libraries to connect to a KDC."""
import os
import time
import clr

clr.AddReference(r"C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference(r"C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference(r"C:\Program Files\Thorlabs\Kinesis\ThorLabs.MotionControl.TCube.DCServoCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.TCube.DCServoCLI import *
from System import Decimal

class Application:
    def __init__(self):
        """The main entry point for the application"""

        # Uncomment this line if you are using
        SimulationManager.Instance.InitializeSimulations()

        # Assign TDC001
        try:
            # Create new device
            self.SN   = "83815209"
            self.ID   = "83"
            serial_no = str(self.SN)             # TDC001 Production ID=83 Production Serial Number=83815209

            DeviceManagerCLI.BuildDeviceList()

            self.TDC001 = TCubeDCServo.CreateTCubeDCServo(serial_no)
            print(DeviceManagerCLI.GetDeviceList())
            # Connect, begin polling, and enable
            self.TDC001.Connect(serial_no)
            time.sleep(0.25)
            self.TDC001.StartPolling(250)
            time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

            self.TDC001.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable

            # Get Device information
            self.device_info = self.TDC001.GetDeviceInfo()
            print(self.device_info.Description)

            # Wait for Settings to Initialise
            if not self.TDC001.IsSettingsInitialized():
                self.TDC001.WaitForSettingsInitialized(10000)  # 10 second timeout
                assert self.TDC001.IsSettingsInitialized() is True

            # Before homing or moving device, ensure the motor's configuration is loaded
            m_config = self.TDC001.LoadMotorConfiguration(serial_no,
                                                    DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
            m_config.DeviceSettingsName = "PRM1-Z7"
            m_config.UpdateCurrentConfiguration()
            self.TDC001.SetSettings(self.TDC001.MotorDeviceSettings, True, False)   
        except:
            print("missing Motor!")

    def P_P(self):                                          #present_position
        #print(f'Device position(Decimal) {self.TDC001.Position}')
        pp = round( float(str(self.TDC001.Position)) *2048/3 ) * (3./2048) 
        #print(f'Device position(float) {pp:.6f}')
        return pp
    
    def Move_Abs(self,set_position):
        # 'MoveTo'
        f = set_position
        d = Decimal(f)
        #print(f'Device moving to position {d} deg')
        self.TDC001.MoveTo(d, 60000)  # 60s timeout again
        time.sleep(2.5)
        return
 
    def Move_Home(self):
        # 'Home'
        print("Homing Actuator")
        self.TDC001.Home(60000)  # 60s timeout, blocking call
        time.sleep(2.5)
        return
    
    def Jog_P01(self):                                      #Jog 0.1deg
        present_position = round( float(str(self.TDC001.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position + 0.1
        d = Decimal(target_position)
        self.TDC001.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return
    
    def Jog_N01(self):                                      #Jog -0.1deg
        present_position = round( float(str(self.TDC001.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position - 0.1
        d = Decimal(target_position)
        self.TDC001.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return

    def Jog_P05(self):                                      #Jog 0.5deg
        present_position = round( float(str(self.TDC001.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position + 0.5
        d = Decimal(target_position)
        self.TDC001.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return
    
    def Jog_N05(self):                                      #Jog -0.5deg
        present_position = round( float(str(self.TDC001.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position - 0.5
        d = Decimal(target_position)
        self.TDC001.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return
    
    def Device_Info(self):  
        return self.device_info.Description
    
    def ID_Number(self):                                #ID
        return self.ID,self.SN
     
    def Device_Disconnect(self):                                      
        self.TDC001.Disconnect()
        print('Device disconnected')
        return
   
if __name__ == '__main__':
    Kinesis_TDC001 = Application()
'''
    pp = Kinesis_TDC001.P_P()
    print(f'P_P Device position {pp:.6f} deg')

    Kinesis_TDC001.Move_Home()
    pp = Kinesis_TDC001.P_P()
    print(f'Move_Home Device position {pp:.6f} deg')

    Kinesis_TDC001.Move_Abs(6.0)
    pp = Kinesis_TDC001.P_P()
    print(f'Move_Abs(6.0) Device position {pp:.6f} deg')

    Kinesis_TDC001.Jog_P05()
    pp = Kinesis_TDC001.P_P()
    print(f'Jog_P05 Device position {pp:.6f} deg')
    Kinesis_TDC001.Jog_P01()
    pp = Kinesis_TDC001.P_P()
    print(f'Jog_P01 Device position {pp:.6f} deg')
    Kinesis_TDC001.Jog_N05()
    pp = Kinesis_TDC001.P_P()
    print(f'Jog_N05 Device position {pp:.6f} deg')
    Kinesis_TDC001.Jog_N01()
    pp = Kinesis_TDC001.P_P()
    print(f'Jog_N01 Device position {pp:.6f} deg')

    Kinesis_TDC001.Move_Abs(345.0)
    pp = Kinesis_TDC001.P_P()
    print(f'Move_Abs(345.0) Device position {pp:.6f} deg')

    device_info = Kinesis_TDC001.Device_Info()
    print('Device_Info',device_info)
    str_ID,str_SN = Kinesis_TDC001.ID_Number()
    print('ID,SN',str_ID,str_SN)
    Kinesis_TDC001.Device_Disconnect()

    '''
# usage example
# import ThorLABS_Kinesis_TDC001_module
#         self.Kinesis_TDC001       = ThorLABS_Kinesis_TDC001_module.Application()
#         self.Kinesis_TDC001.Move_Abs(3.0)
#         Present_Position  = Kinesis_TDC001.P_P()
