import pyvisa as visa

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            self.rm = visa.ResourceManager('@py')
            self.instrument = self.rm.open_resource('GPIB0::3::INSTR')
        except:
            print('Error: Agilent 34410A(GPIB address::3) not Found ')  

    # Measure 
    def Measure(self):
        self.instrument.write( 'MEASure:VOLTage:DC?' )
        value      = float(self.instrument.read())
        # End Agilent34410A
        #print("Value = ",value )
        return value
    
    # Simple Read Buffer read
    def Read(self):
        value      = float(self.instrument.query('READ?'))
        # End Agilent34410A
        #print("Value (READ)= ",value )
        return value 
        # Simple Read Buffer read

    def GoToLocal(self):
        self.rm.close()
        #self.instrument.write( '*RST' )
        return
    
    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        print("query *IDN? = ",str_ID )
        return str_ID
    
if __name__ == '__main__':
    Agilent34410A = Application()
    '''
    value2 = Agilent34410A.Measure()
    print("Reprint2 \n Value = ",value2)
    Agilent34410A.ID_Number()
    Agilent34410A.Read()
    Agilent34410A.GoToLocal()
'''
# usage example
# import Agilent34410A_read_module
#         self.Agilent34410A    = Agilent34410A_read_module.Application()
#         value  = self.Agilent34410A.Measure()
#         str_ID = self.Agilent34410A.ID_Number() 