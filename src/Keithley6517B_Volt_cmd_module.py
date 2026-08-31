import pyvisa as visa
#import tkinter as tk

class Application:
    def __init__(self):
        
        try:
            #　計測機器と通信処置
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource('GPIB0::27::INSTR')
        except:
            print('Error: Keithley6517B(GPIB address::27) not Found ')

        try:
            #　Configuration Set　　　　:SOURce:VOLTage:RANGe <n> Select V-Source range　　@20230821
            self.instrument.write( ':SOUR:VOLT:RANG MAX;')  #RANGe MAXimum (=1000V)
            str_value = self.instrument.query( ':SOUR:VOLT:RANG?;')
            print("@Method __int__,  RANGe_query = ",str_value)
        except:
            print(' Query(Range?) error : Keithley6517B not resposed ')

    # KE6517B Voltage Status Read
    def V_Status(self):
        self.instrument.write( ':SOUR:VOLT:LEV:IMM:AMPL?;')
        str_value = self.instrument.read()
        volts_read  = float(str_value.split(',', 3)[0])  #  ←インデックス番号0番を取り出す
        # End Keithley 6517B
        #print("@Method Measure,  Voltage_read = ",volts_read)
        return volts_read

    # KE6517B Voltage Write 
    def V_Write(self,volts_target):
        str_text = ':SOUR:VOLT ' + str( volts_target )
        self.instrument.write( str_text )                           #  ←KE6517B　書込み
        return

    # KE6517B Voltage Operate On/Off 
    def V_Operate(self):
        self.instrument.write( ':MANual:VSOurce:OPERate;')  #OPERate command Enable or disable V-Source output
        return
    ''' 
    :MANual 自動電圧源抵抗設定用パス：
        :VSOurce 電圧源設定用パス：
            [:AMPLitude] <n> 電圧源レベルを指定（0～1000）
            :RANGe <n> レンジ設定：≤100 = 100V レンジ、>100 = 1000V レンジ
            :OPERate <b> 電圧源出力のオン/オフ
    '''
    # ID number query    
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        #print("@Method ID_Number,  ID_Number = ",str_ID)
        return str_ID

if __name__ == '__main__':
    KE6517B = Application()

    #KE6517B.ID_Number()
    #KE6517B.V_Status()
    #KE6517B.V_Write(5)
   #KE6517B.V_Write(0)

# usage example
# import Keithley6517B_Volt_cmd_module
#         self.KE6517B     = Keithley6517B_Volt_cmd_module.Application()
#         volts_read  = self.KE6517B.V_Status() 
#         self.KE6517B.V_Write(volts_target)
#         volts_read  = self.KE6517B.V_Status() 
