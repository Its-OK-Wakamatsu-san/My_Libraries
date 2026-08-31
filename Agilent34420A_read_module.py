import pyvisa as visa

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource('GPIB0::22::INSTR')
        except:
            print('Error: Agilent 34420A(GPIB address::22) not Found ')  

    # Measure 
    def Measure(self):
        self.instrument.write( 'MEASure:VOLTage:DC?' )
        value      = float(self.instrument.read())
        # End Agilent34420A
        #print("Value = ",value )
        return value
    
    # Simple Read 
    def Read(self):
        value      =float(self.instrument.query('READ?'))
        # End Agilent34420A
        #print("Value (READ)= ",value )
        return value 
    
    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        #print("query *IDN? = ",str_ID )
        return str_ID
    
if __name__ == '__main__':
    Agilent34420A = Application()
    
    '''
    value2 = Agilent34420A.Measure()
    print("Reprint2 \n Value = ",value2)
    Agilent34420A.ID_Number()
    Agilent34420A.Read()
'''

# usage example
# import Agilent34420A_read_module
#         self.Agilent34420A    = Agilent34420A_read_module.Application()
#         value  = self.Agilent34420A.Read()
#         str_ID = self.Agilent34420A.ID_Number() 