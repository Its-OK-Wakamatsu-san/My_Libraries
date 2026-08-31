import serial
import time

# comunicate with MATSUSADA_PRK10_150 via Matsusada USB-OPT(USB adapter for optical communication)
# https://www.matsusada.co.jp/product/power-supplies/accessories/gp/

class Application:
    def __init__(self):
        #cr_data= [0x0D] # byte array
        #print(cr_data) # print出力すると10進表記になる #[13]
        # Convert byte-array to Binary
        #cr_b =bytes(cr_data) 
        #print(cr_b)
        self.cr_b = b'\r' # cr:terminal code = b'\r' or [0x0D]
        #print(self.cr_b)        #b'\r'

    def Connect_Device(self):
        try:
            self.serial_port = serial.Serial(
                port='COM9',\
                baudrate=9600,\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                timeout=100 )
            #print("connected to: " + self.serial_port.portstr)                       #CHG COM9
            #setting = self.serial_port.get_settings()
            #print("Serial Setting is : ",setting)
        except:
            print('Error: MASTUSADA_Optical_USB_Module not Found ') 
        return
    #
    def Set_Command(self,cmd_ASCII):
        self.Connect_Device()
        cmd_b =cmd_ASCII.encode() + self.cr_b
        #print(cmd_b)
        self.serial_port.write(cmd_b)
        time.sleep(0.05)      
        self.serial_port.close()
        return
    
    def Command_Response(self,cmd_ASCII):
        self.Connect_Device()
        cmd_b =cmd_ASCII.encode() + self.cr_b
        #print(cmd_b)
        self.serial_port.write(cmd_b)
        time.sleep(0.10)            # need to wait minimum 0.05sec
        buf = self.serial_port.read_all()
        buf_ASCII = buf.decode()
        self.serial_port.close()
        return buf_ASCII
    
if __name__ == '__main__':
    MATSUSADA_USB = Application()

    time_A = time.time()

    MATSUSADA_USB.Set_Command('#AL GTL')
    buf = MATSUSADA_USB.Command_Response('#1 STS')
    print(buf)
    time_B = time.time()
    elapsed_time = time_B - time_A
    print('elapsed_time =', elapsed_time)

    '''
    #AL .. all unit
    #1  .. unit1
    #2  .. unit2

    '#AL REN'       # Cmd Change Local to Remote
    '#AL VCN 100'   # Cmd Set Voltage CNTL(%)
    '#AL OCP 100'   # Cmd Set Over Current(%)
    '#AL ISET 0.0'  # Cmd Set Current 0.0(A)    ... Constant Current Mode
    '#AL SW1'       # Cmd Switch on             ... 1..On
    '#1 STS'        # Query No.1unit status        
    '#2 STS'        # Query No.2unit status
    '#1 ISET 5.0'   # Cmd Set Current 5.0(A)  No.1unit ... Constant Current Mode
    '#2 ISET 5.0'   # Cmd Set Current 5.0(A)  No.2unit ... Constant Current Modes
    '#1 VGET'       # Query No.1unit voltage(V)
    '#1 IGET'       # Query No.1unit current(A)
    '#2 VGET'       # Query No.2unit voltage(V)
    '#2 IGET'       # Query No.2unit current(A)
    '#AL SW0'       # Cmd Switch off             ... 0..Off
    '#AL GTL'       # Cmd Change Remote to Local

    '''
