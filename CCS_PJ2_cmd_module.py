import pyvisa as visa
import time

class Application:
    def __init__(self):
        try:
            #   ether通信    See.   https://otonarika.tech/python-ethernet/  
            #　ether機器と通信処置          Set IP Address on PC    PC=TCPIP::192.168.0.16,     GW=TCPIP::192.168.0.1
            self.rm = visa.ResourceManager('@py')
            self.rm.list_resources()
            self.instrument = self.rm.open_resource("TCPIP::192.168.0.2::40001::SOCKET")  #  40001 is port No.
        except:
            print('Error: CCS PJ2 LED Controller(TCPIP::192.168.0.2::40001::SOCKET) not Found ')

        #終端子を指定
        self.instrument.read_termination  = '\r\n'     # <CR><LF>
        self.instrument.write_termination = '\r\n'
        time.sleep(0.200)
        # LED Lamp Initialized    
        self.instrument.write("@00L1")   
        # Etherのwriteに掛かる時間  Elapsed Time / 1 write Command     ≒ 200ms/1command @ Ether経由
 
    def Light_Status(self):
        self.instrument.write("@00M")       # Confirm LED Status command
        str_text  = self.instrument.read()
        # pick up Light intensity strings
        str_light = str_text[5:9]           # read sample ...."@00OF0123L1ID00"    light_intensity....."0123"
        return  str_text , str_light        # def Light_Status() -> Return str_text , str_light

    # light_intensity -> light_strings Command with Limmiter
    def Light_Str(self, light_intensity):
        # 4桁表示処置
        if  light_intensity < 0:
            light_intensity = 0
            str_light = "0000"
        if  light_intensity > 900:             # Intensity is available in (0-1024). But Sets Limitter : 900 ≒ 900mA
            light_intensity = 900
            str_light = str( light_intensity )
        if 0 <= light_intensity < 10:  # and演算子を省略
            str_light = "000" + str(light_intensity)
        if 10 <= light_intensity < 100:  # and演算子を省略
            str_light = "00" + str(light_intensity)
        if 100 <= light_intensity < 1000:  # and演算子を省略
            str_light = "0" + str(light_intensity)
        return str_light

    # Set Light Intensity  
    def Set_Light(self,light_target):
        light_now =  light_target
        str_light = self.Light_Str( light_now )
        self.instrument.write( "@00F" + str_light )            # Set Light Intensity command
        #time.sleep(self.wait_time)      # wait_time  sec待つ   ≒ 200ms/1command ＠Ether経由
        return

    #通信を切断する
    def Close_Instrument(self):
        try:
            self.rm.close()
        except:
            print('Close Error: CCS PJ2 LED Controller not Found ')
        return

if __name__ == '__main__':
    LED = Application()
    '''
    str_text , str_light = LED.Light_Status()
    print("Reprint \n @ Method Light_Status str_light = ",str_light)
    LED.Set_Light(light_target=10)
    str_text , str_light = LED.Light_Status()
    print("Reprint \n @ Method Light_Status str_light = ",str_light)
    LED.Set_Light(light_target=0)
    str_text , str_light = LED.Light_Status()
    print("Reprint \n @ Method Light_Status str_light = ",str_light)
'''
# usage example
# import CCS_PJ2_cmd_module
#         self.LED = CCS_PJ2_cmd_module.Application()
#         str_text , str_light = self.LED.Light_Status()
#         self.LED.Set_Light(light_target=10)        #0-900(1024) means 0-900mA(1000mA)

