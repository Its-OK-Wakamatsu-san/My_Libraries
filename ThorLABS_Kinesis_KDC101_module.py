# from https://github.com/Thorlabs/Motion_Control_Examples/blob/main/Python/KCube/KDC101/kdc101_pythonnet.py
"""An example that uses the .NET Kinesis Libraries to connect to a KDC."""
import os
import time
import clr

clr.AddReference(r"C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference(r"C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference(r"C:\Program Files\Thorlabs\Kinesis\ThorLabs.MotionControl.KCube.DCServoCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from System import Decimal

class Application:
    def __init__(self):
        """The main entry point for the application"""

        # Uncomment this line if you are using
        SimulationManager.Instance.InitializeSimulations()

        # Assign KDC101
        try:
            # Create new device
            self.SN   = "27000001"               # change 27000001-> 27______ 
            self.ID   = "27"
            serial_no = str(self.SN)             # KDC101 Production ID=27 Production Serial Number=27______  ??

            DeviceManagerCLI.BuildDeviceList()

            self.KDC101 = KCubeDCServo.CreateKCubeDCServo(serial_no)
            print(DeviceManagerCLI.GetDeviceList())
            # Connect, begin polling, and enable
            self.KDC101.Connect(serial_no)
            time.sleep(0.25)
            self.KDC101.StartPolling(250)
            time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

            self.KDC101.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable

            # Get Device information
            self.device_info = self.KDC101.GetDeviceInfo()
            print(self.device_info.Description)

            # Wait for Settings to Initialise
            if not self.KDC101.IsSettingsInitialized():
                self.KDC101.WaitForSettingsInitialized(10000)  # 10 second timeout
                assert self.KDC101.IsSettingsInitialized() is True

            # Before homing or moving device, ensure the motor's configuration is loaded
            m_config = self.KDC101.LoadMotorConfiguration(serial_no,
                                                    DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
            m_config.DeviceSettingsName = "PRM1-Z7"                     #Device Name______ ??
            m_config.UpdateCurrentConfiguration()
            self.KDC101.SetSettings(self.KDC101.MotorDeviceSettings, True, False)   
        except:
            print("missing Motor!")

    def P_P(self):                                          #present_position
        #print(f'Device position(Decimal) {self.KDC101.Position}')
        pp = round( float(str(self.KDC101.Position)) *2048/3 ) * (3./2048) 
        #print(f'Device position(float) {pp:.6f}')
        return pp
    
    def Move_Abs(self,set_position):
        # 'MoveTo'
        f = set_position
        d = Decimal(f)
        #print(f'Device moving to position {d} deg')
        self.KDC101.MoveTo(d, 60000)  # 60s timeout again
        time.sleep(2.5)
        return
 
    def Move_Home(self):
        # 'Home'
        print("Homing Actuator")
        self.KDC101.Home(60000)  # 60s timeout, blocking call
        time.sleep(2.5)
        return
    
    def Jog_P01(self):                                      #Jog 0.1deg
        present_position = round( float(str(self.KDC101.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position + 0.1
        d = Decimal(target_position)
        self.KDC101.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return
    
    def Jog_N01(self):                                      #Jog -0.1deg
        present_position = round( float(str(self.KDC101.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position - 0.1
        d = Decimal(target_position)
        self.KDC101.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return

    def Jog_P05(self):                                      #Jog 0.5deg
        present_position = round( float(str(self.KDC101.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position + 0.5
        d = Decimal(target_position)
        self.KDC101.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return
    
    def Jog_N05(self):                                      #Jog -0.5deg
        present_position = round( float(str(self.KDC101.Position)) *2048/3 ) * (3./2048)    # check PP
        target_position  = present_position - 0.5
        d = Decimal(target_position)
        self.KDC101.MoveTo(d, 10000)  # 10s timeout again
        time.sleep(2)
        return
    
    def Device_Info(self):  
        return self.device_info.Description
    
    def ID_Number(self):                                #ID
        return self.ID,self.SN
     
    def Device_Disconnect(self):                                      
        self.KDC101.Disconnect()
        print('Device disconnected')
        return
   
if __name__ == '__main__':
    Kinesis_KDC101 = Application()
'''
    pp = Kinesis_KDC101.P_P()
    print(f'P_P Device position {pp:.6f} deg')

    Kinesis_KDC101.Move_Home()
    pp = Kinesis_KDC101.P_P()
    print(f'Move_Home Device position {pp:.6f} deg')

    Kinesis_KDC101.Move_Abs(6.0)
    pp = Kinesis_KDC101.P_P()
    print(f'Move_Abs(6.0) Device position {pp:.6f} deg')

    Kinesis_KDC101.Jog_P05()
    pp = Kinesis_KDC101.P_P()
    print(f'Jog_P05 Device position {pp:.6f} deg')
    Kinesis_KDC101.Jog_P01()
    pp = Kinesis_KDC101.P_P()
    print(f'Jog_P01 Device position {pp:.6f} deg')
    Kinesis_KDC101.Jog_N05()
    pp = Kinesis_KDC101.P_P()
    print(f'Jog_N05 Device position {pp:.6f} deg')
    Kinesis_KDC101.Jog_N01()
    pp = Kinesis_KDC101.P_P()
    print(f'Jog_N01 Device position {pp:.6f} deg')

    Kinesis_KDC101.Move_Abs(345.0)
    pp = Kinesis_KDC101.P_P()
    print(f'Move_Abs(345.0) Device position {pp:.6f} deg')

    device_info = Kinesis_KDC101.Device_Info()
    print('Device_Info',device_info)
    str_ID,str_SN = Kinesis_KDC101.ID_Number()
    print('ID,SN',str_ID,str_SN)
    Kinesis_KDC101.Device_Disconnect()

    '''
# usage example
# import ThorLABS_Kinesis_KDC101_module
#         self.Kinesis_KDC101       = ThorLABS_Kinesis_KDC101_module.Application()
#         self.Kinesis_KDC101.Move_Abs(3.0)
#         Present_Position  = Kinesis_KDC101.P_P()
