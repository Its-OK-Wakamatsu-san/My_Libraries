import pyvisa as visa

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource('GPIB0::24::INSTR')
        except:
            print('Error: Keithley2400(GPIB address::24) not Found ')

    # Measure Voltage
    def Measure_V(self):
        # Measure voltage on Keithley 2400
        self.instrument.write(':MEASure:VOLTage:DC?')
        str_status      = self.instrument.read()
        str_status_0 =str_status.split(',', 4)[0]           #  ←','で4分割、インデックス番号0番を取り出す
        voltage = float(str_status_0 )
        return voltage

    def Set_V(self,voltage):
        # Set voltage on Keithley 2400
        str_volt = str(voltage)                             # V
        self.instrument.write( ':SOUR:VOLT '+str_volt)
        self.instrument.write(':MEASure:VOLTage:DC?')
        str_Aout_value  = self.instrument.read()
        str_status_0 =str_Aout_value.split(',', 4)[0]       #  ←','で4分割、インデックス番号0番を取り出す
        voltage = float(str_status_0 )
        return voltage 

    def Measure_I(self):
        # Measure current on Keithley 2400
        self.instrument.write(':MEASure:CURRent:DC?')
        str_status      = self.instrument.read()
        str_status_0 =str_status.split(',', 4)[0]           #  ←','で4分割、インデックス番号0番を取り出す
        current_mA = float(str_status_0 )*1000              #mA
        return current_mA
        
    def Set_I(self,current_mA):
        # Set current on Keithley 2400
        str_current = str(current_mA/1000.0)                #mA
        self.instrument.write( ':SOUR:CURRent:'+ str_current)
        self.instrument.write(':MEASure:CURRent:DC?')
        str_Aout_value  = self.instrument.read()
        str_status_0 =str_Aout_value.split(',', 4)[0]       #  ←','で4分割、インデックス番号0番を取り出す
        current_mA = float(str_status_0 )*1000.0            #mA
        return current_mA

    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        return str_ID
    
    # Reset
    def Source_Reset(self):
        self.instrument.write('*RST')
        return
    
    # Disconnect
    def GoToLocal(self):
        self.instrument.close()
        #self.instrument.write( '*RST' )
        return
    
if __name__ == '__main__':
    KE2400 = Application()
    '''
    str_ID = KE2400.ID_Number()
    print("ID = ",str_ID)
    current_mA = KE2400.Set_I(0.001) #mA
    print("Out_value current(mA) = ",current_mA)
    current_mA = KE2400.Measure_I()
    print("Measured current(mA) = ",current_mA)
    voltage = KE2400.Set_V(0.025) #V
    print("Out_value voltage(V) = ",voltage)
    voltage = KE2400.Measure_V()
    print("Measured voltage(V) = ",voltage)
    voltage = KE2400.Set_V(0.0)
    print("Out_value voltage(V) = ",voltage)
    KE2400.Source_Reset()
    print("Reset ")
    '''

# usage example
# import Keithley2400_module
#         self.KE2400   = Keithley2400_module.Application()
#         voltage       = self.KE2400.Measure_V() 