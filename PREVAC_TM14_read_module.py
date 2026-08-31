# https://qiita.com/Gyutan/items/150c9fac57f7380a1763
import serial
import struct 
import time

# PREVAC TM14 serial comunication,

class Application:
    def __init__(self):
        #self.req_cmd  = 'AA04C8A1C80153010000008A0D'  # 8A:CRC 0D:carriage return(termination code)
        senddata=[0xAA,0x04,0xC8,0xA1,0xC8,0x01,0x53,0x01,0x00,0x00,0x00,0x8A,0x0D]
        #print(senddata)          #[170, 4, 200, 161, 200, 1, 83, 1, 0, 0, 0, 138, 13]
        #Convert byte-array to Binary
        self.send_binary =bytes(senddata) 
        #print(self.send_binary)
        send_b = b'\xaa\x04\xc8\xa1\xc8\x01S\x01\x00\x00\x00\x8a\r'

    def Connect_Device(self):
        try:
            self.serial_port = serial.Serial(
                port='COM2',\
                baudrate=57600,\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                timeout=500 )
            #print("connected to: " + self.serial_port.portstr)                       #CHG COM3 temporary
            setting = self.serial_port.get_settings()
            #print("Serial Setting is : ",setting)
        except:
            print('Error: PREVAC_TM14 not Found ') 
        return
    
    def Connect_Device_Test(self):
        try:
            self.serial_port = serial.Serial(
                port='COM2',\
                baudrate=57600,\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                timeout=500 )
            print("connected to: " + self.serial_port.portstr)                       #CHG COM3 temporary
            setting = self.serial_port.get_settings()
            print("Serial Setting is : ",setting)
            self.serial_port.close()
        except:
            print('Error: PREVAC_TM14 not Found ') 
        return
    # receive frequency data
    def Read_Frequency(self):
        self.Connect_Device()
        self.serial_port.write(self.send_binary)
        time.sleep(0.02)      
        buf_full = self.serial_port.read_all()
        #print('buf_full =',buf_full)                            #b'\xaa\t\x01\xa1\xc8\xc8S#\xb1\xae1\x01\x9d\x00d\x0eQ'           
        reply = struct.unpack('17B',buf_full)
        #print('reply = ',reply)                #reply =  (170, 9, 1, 161, 200, 200, 83, 35, 177, 174, 49, 1, 157, 0, 100, 14, 81)
        freq = reply[7:11]
        #print('freq = ',freq)                  #freq =  (35, 177, 174, 49)
        # 32bit 符号なし整数に変換する場合（ビッグエンディアン）
        ulong_value = struct.unpack('>L', bytes(freq))
        frequency = int(ulong_value[0])/100
        self.serial_port.close()
        #print('self.serial_port.close() .... disconnected')
        return frequency
    
if __name__ == '__main__':
    PREVAC_TM14 = Application()

    '''
    time_A = time.time()
    frequency = PREVAC_TM14.Read_Frequency()
    print('freq(Hz)= ',frequency)
    time_B = time.time()
    elapsed_time = time_B - time_A
    print('elapsed_time =', elapsed_time)
    '''
# usage example
# import PREVAC_TM14_read_module
#        #Define instance from Imported Instrument module and Class
#         self.PREVAC_TM14     = PREVAC_TM14_read_module.Application()
#         frequency = self.PREVAC_TM14.Read_Frequency()