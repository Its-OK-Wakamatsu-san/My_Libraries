import pyvisa as visa
import tkinter as tk

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource('GPIB0::2::INSTR')
        except:
            print('Error: NF LI5640(GPIB address::2) not Found ')  
        
        # Call Once when assigned this instrument    
        self.instrument.write( 'APHS;')  # add AutoPhase @20230823

    # Measure Click
    def Measure(self):
        # Manual_Sensitivity......Tuple
        self.Manual_Sensitivity_module = ('2nV', '5nV', '10nV','20nV', '50nV', '100nV','200nV', '500nV', '1uV','2uV', '5uV', '10uV','20uV', '50uV', '100uV','200uV', '500uV', '1mV','2mV', '5mV', '10mV','20mV', '50mV', '100mV','200mV', '500mV', '1V')
        self.Manual_Sensitivity_v = tk.StringVar()

        # 計測機器と通信処置  Write & Read Cmdの送出
        self.instrument.write( 'OTYP 1,2,4,5;OSMP 0.1; OSTR 0; DOUT?')  #Delete AutoPhase here and Add in __init__ @20230823
        str_value  = self.instrument.read()
        volts      = float(str_value.split(',', 3)[0])  #  ←','で4分割、インデックス番号0番を取り出す
        theta      = float(str_value.split(',', 3)[1])  #  ←','で4分割、インデックス番号1番を取り出す
        vsen       = int(str_value.split(',', 3)[2])    #  ←','で4分割、インデックス番号2番を取り出す
        vsen_tuple = self.Manual_Sensitivity_module[vsen]
        status   = int(str_value.split(',', 3)[3])      #  ←','で4分割、インデックス番号3番を取り出す
        if status == 0:
            str_status = ' Working correctly '
        else:
            str_status = ' Overflow occurred '

        #　計測機器と通信処置 terminate
        #rm.close()
        return volts, theta, vsen_tuple, str_status
    
    # Auto Phase Command
    def Auto_Phase(self):  
        self.instrument.write( 'APHS;')  # add AutoPhase @20230908
        return 

    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        return str_ID
    
if __name__ == '__main__':
    NF5640 = Application()
    root = tk.Tk()
    volts, theta, vsen_tuple, str_status = NF5640.Measure()
    print("Reprint2 \n Voltage(V) = ",volts, ", Theta = ",theta, ", Sensitivity = ", vsen_tuple, ", Status = ",str_status)
   
    NF5640.Measure()

# usage example
# import NF_LI5640_read_module
#         self.NF5640     = NF_LI5640_read_module.Application()
#         volts, theta, vsen_tuple, str_status  = self.NF5640.Measure() 