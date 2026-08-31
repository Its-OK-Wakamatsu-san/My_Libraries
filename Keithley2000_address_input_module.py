import pyvisa as visa

class Application:
    def __init__(self,str_address):      # pass the argument(str_address) to the Class. 'GPIB0::16::INSTR' , 'GPIB0::17::INSTR' , 'GPIB0::19::INSTR'
        try:
            # 計測機器と通信処置      
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource(str_address)        
        except:
            print ('KE2000 address= ' ,str_address,'is not found.')     

        # Call Once when assigned this instrument  @20230823
        # add NPLC(Number of Power Line Cycles)=1 , that means 60Hz reading, and max speed reading.
        print('Keithley 2000(Address=',str_address,') is connected.')
        str_text = ":FUNC 'VOLT:DC'; :VOLT:DC:NPLC 1;"   
        self.instrument.write(str_text)

    # Measure 
    def Measure(self):
        self.instrument.write(':FORM:ELEM READ,CHAN,UNIT;:FETCH?')
        str_status      = self.instrument.read()
        str_status_0    = str_status.split(',', 1)[0]     #  ←','で2分割、インデックス番号0番を取り出す
        str_status_1    = str_status.split(',', 1)[1]     #  ←','で2分割、インデックス番号1番を取り出す
        value           = float( str_status_0[:15] )
        unit            = str_status_0[15:]
        channel         = int( str_status_1[:2] )
        # End Keithley 2000
        # print("Value = ",value, ",Unit = ",unit, ",Channel = ", channel)

        return value, unit, channel

    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        return str_ID
    
if __name__ == '__main__':
    KE2000 = Application()

    #value2, unit2, channel2 = KE2000.Measure()
    #print("Reprint2 \n Value = ",value2, ",Unit = ",unit2, ",Channel = ", channel2)
   
    #KE2000.Measure()

# usage example
# import Keithley2000_read_module
#         self.KE2000     = Keithley2000_read_module.Application('GPIB0::16::INSTR')
#         value, unit, channel  = self.KE2000.Measure() 