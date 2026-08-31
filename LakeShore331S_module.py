import pyvisa as visa
import time

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource('GPIB0::12::INSTR') # LakeShore331S
        except:
            print('Error: LakeShore 331S(GPIB address::12) not Found ')

    # Measure Click
    def Measure(self):
        # 計測機器と通信処置  Write & Read Cmdの送出
        self.instrument.write( "INTYPE A,7,0" ) # INTYPE <input>, <sensor type>, <compensation> #<sensor type>=7  = Thermocouple 50 mV(for hightemp>500K)
        #self.instrument.write( "INTYPE B,1,0" ) # <sensor type>=1 = GaAlAs Diode
        self.instrument.write( 'CRDG?')             # Celsius Reading Query
        str_value  = self.instrument.read()
        celsius      = float(str_value) 
        self.instrument.write( 'KRDG?')             # Kervin Reading Query
        str_value  = self.instrument.read()
        kelvin      = float(str_value) 

        self.instrument.write( "INCRV?" )
        str_ID_n_curve  = self.instrument.read()
        self.instrument.write( "INTYPE? A" )
        str_ID_n_type  = self.instrument.read()

        return celsius, kelvin, str_ID_n_curve, str_ID_n_type
    # Measure Click

    def Set(self,voltage):
        # 計測機器と通信処置  Write & Read Cmdの送出

        str_volt = str(float(voltage)*10.0) #0-10V -> 0-100%
        self.instrument.write( 'CMODE 2,1')
        str_set_analog = "ANALOG 0, 2, A, 1, 100.0, 0.0, "  #Input: ANALOG <bipolar enable>, <mode>, <input>, <source>, <high value>, <low value>, <manual value>[term]
        self.instrument.write(str_set_analog + str_volt)    #For Analog Output Parameter Command (Output2)
        #self.instrument.write( 'ANALOG?')
        #str_Analogout  = self.instrument.read()
        #print(str_Analogout)
        #self.instrument.write( 'MOUT 1 ' + str_volt)　　　　#For Heater Manual output Command (Output1) 
        #self.instrument.write( 'MOUT? 1')
        #str_Mout_value  = self.instrument.read()
        time.sleep(0.3)                                     #300ms #DELAY
        self.instrument.write( 'AOUT?')
        str_Aout_value  = self.instrument.read()
        #self.instrument.write( 'DFLT 99')                  #DFLT Factory Defaults Command

        return str_Aout_value
    
    # Thermocouple Input Ranges Calibration
    def Calibrate(self):
        #1st Step
        '''
        # 計測機器と通信処置  Write & Read Cmdの送出
        self.instrument.write( "CALRSTZ A,7" ) # Zero Offset Reset Command: <input>, <sensor type> #<sensor type>=7  = Thermocouple 50 mV(for hightemp>500K)
        self.instrument.write( "CALRSTG A,7" ) # Gain Reset Command: <input>, <sensor type>
        # Short the V+ and V– terminals together
        self.instrument.write( 'CALREAD?')
        str_CALREAD_value  = self.instrument.read()
        print("Thermocouple Input Ranges Calibration \n  str_CALREAD_value = ",str_CALREAD_value)

        #Thermocouple Input Ranges Calibration 
        #  str_CALREAD_value =  -00.0889
        '''
        #2nd Step 
        # Notes!
        # Zero Calibration was not performed correctly even though followed the users manual. 
        # So, connected K-type Thermocouple, and adjusted Zero-Point so that indicator was equal to room temperature.
        '''
        #self.instrument.write( 'CALZ A,7, 1.000')  # <-- equal to room temperature
        #self.instrument.write( 'CALREAD?')
        #str_CALREAD_value  = self.instrument.read()
        #print("Thermocouple Input Ranges Calibration \n  str_CALREAD_value = ",str_CALREAD_value)        
        #Thermocouple Input Ranges Calibration 
        #  str_CALREAD_value =  -00.0005
        '''
        #3rd Step
        '''
        self.instrument.write( 'CALREAD?')
        str_CALREAD_value  = self.instrument.read()
        print("Thermocouple Input Ranges Calibration \n  str_CALREAD_value = ",str_CALREAD_value)
        #Thermocouple Input Ranges Calibration  Vsource = 49.04
        #str_CALREAD_value =  +49.8444
        #+49.73/+49.8444 =1.018087
        '''
        #4th Step       
        '''
        #self.instrument.write( 'CALG A,7,1.000')
        self.instrument.write( 'CALREAD?')
        str_CALREAD_value  = self.instrument.read()
        print("Thermocouple Input Ranges Calibration \n  str_CALREAD_value = ",str_CALREAD_value)
        '''
        #5th Step
        #self.instrument.write('CALSAVE')
        return
    
    # ID number query    
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        return str_ID
    
if __name__ == '__main__':
    LS331S = Application()
    #LS331S.Calibrate()
    #celsius, kelvin, str_ID_n_curve,str_ID_n_type = LS331S.Measure()
    #print("Method LS331S.Measure \n Celsius() = ",celsius, ", Kelvin = ",kelvin," str_ID_n_curve = ",str_ID_n_curve, ", str_ID_n_type = ", str_ID_n_type)
    #str_Aout_value = LS331S.Set(2.0)
    #print("Method LS331S.Set \n  str_Aout_value = ",str_Aout_value)
    #print("ID number = ", LS331S.ID_Number())

# usage example
# import LakeShore331S_module
#        #Define instance from Imported Instrument module and Class
#         self.LS331S     = LakeShore331S_module.Application()
#         celsius, kelvin, str_ID_n_curve,str_ID_n_type   = self.LS331S.Measure() 