# https://github.com/TurBoss/TurBoHostLink
import serial
import time
from functools import reduce
from operator import xor

#OMRON G3PW, serial comunication, CompoWay/F(miniFINS) protocol

class Application:
    def __init__(self):
        # command break down   _typical command_    read the model number and buffer size 
        self.cmd_stx_b =  b'\x02'       # start of text
        self.cmd_0  = '01000'           # NODE:01 SubAddress:00 SID:0
        self.cmd_1  = '0503'            # MRC/SRC(MainRequestCode/SubRequestCode)  
        self.cmd_1A = '0101'            # MRC/SRC(MainReponseCode/SubReponseCode)
        self.cmd_2  = 'CE0001000001'    # internal power gradient
        self.cmd_etx_b =  b'\x03'       # end of text 

    def Connect_Device(self):
        try:
            self.serial_port = serial.Serial(
                port='COM1',\
                baudrate=57600,\
                parity=serial.PARITY_EVEN,\
                stopbits=serial.STOPBITS_TWO,\
                bytesize=serial.SEVENBITS,\
                timeout=0 )
            #print("connected to: " + self.serial_port.portstr)                       #CHG COM3 temporary,  CompoWay/F default baudrate is 57600bps 
            setting = self.serial_port.get_settings()
            #print("Serial Setting is : ",setting)
        except:
            print('Error: OMRON_G3PW not Found ') 
        return
    
    # FCS                      copy from  https://github.com/TurBoss/TurBoHostLink
    def Compute_FCS(self, msg):
        return format(reduce(xor, map(ord, msg)), '01x')                #CHG 'x' → '01x'. Output is string.
    
    # write Command & read G3PW buffer
    def Command_Response(self, cmd):
        cmd_ASCII = self.cmd_0 + cmd + self.cmd_etx_b.decode()          # cmd in ASCII characters

        fcs = self.Compute_FCS( cmd_ASCII )                             # calculate cmd_ASCII XOR
        fcs_h = int(fcs,16)                                             #INS  change hex_string → integer
        bcc_b = fcs_h.to_bytes(1, byteorder='big')                      #INS  change integer    → bainary
        cmd_b = self.cmd_stx_b + cmd_ASCII.encode() + bcc_b
        
        self.Connect_Device()
        self.serial_port.write(cmd_b)
        time.sleep(0.05)                                    # Wait a minute (0.05s).    tried minimum wait time  ... about 0.05s
        
        buf = self.serial_port.read()                       # read start of text         stx_b =  b'\x02' dummy read
        buf_full = self.serial_port.read_all()
        buf_full_ASCII = buf_full.decode()                      #01000005030000G3PW-A12030071
        buf_ASCII = buf_full_ASCII[10:]                         #0123456789012345678901234567890
        self.serial_port.close()
        return buf_ASCII
    
    def Device_Info(self):  
        cmd       = '0503'         # read the model number and buffer size  MRC/SRC(MainRequestCode/SubRequestCode)
        buf_ASCII = self.Command_Response(cmd)                  #05030000G3PW-A12030071                              
        str_ID = buf_ASCII[4:14]                                #0123456789012345678901234
        return str_ID
    
    def Type_Command_Respose(self,cmd_type): 
        cmd_base  = '0101'         # MRC/SRC(MainReponseCode/SubReponseCode)
        cmd = cmd_base + cmd_type
        buf_ASCII = self.Command_Response(cmd)                  #0000000003E8|         
        str_output = buf_ASCII[4:12]                            #0123456789012345678901234
        output = float(int(str_output,16))/10
        return output

if __name__ == '__main__':
    OMRON_G3PW = Application()

    # usage example
    # import OMRON_G3PW_module
    #         self.OMRON_G3PW   = OMRON_G3PW_module.Application()
    #         str_ID            = self.OMRON_G3PW.Device_Info() 
