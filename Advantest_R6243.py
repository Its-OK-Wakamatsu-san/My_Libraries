import pyvisa as visa

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            self.rm = visa.ResourceManager('@py')
            self.instrument = self.rm.open_resource('GPIB0::19::INSTR')
        except:
            print('Error: Advantest R6243(GPIB address::19) not Found ')  

    # Set Current Limit   default=0.5A
    def Set_Current_Limit(self,current_limit):
        str_current_limit = str(current_limit)
        self.instrument.write( 'VF' )   #Voltage Source Function
        str_command    = "D" + str_current_limit + "MA"
        self.instrument.write( str_command )   #Current Limit Command
        # End Advantest R6243 
        return
    
    # Set Voltage Limit   
    def Set_Votage_Limit(self,voltage_limit):
        str_voltage_limit = str(voltage_limit)
        self.instrument.write( 'IF' )   #Current Source Function
        str_command    = "D" + str_voltage_limit + "V"
        self.instrument.write( str_command )   #Voltage Limit Command
        # End Advantest R6243 
        return
    
    # Voltage Source Command
    def Set_Voltage(self,volt):
        str_volt = str(volt)
        #self.instrument.write( 'MD0' )  #DC Source Mode
        #self.instrument.write( 'VF' )   #Voltage Source Function
        #self.instrument.write( 'V5' )   #Voltage Range 32V range
        str_command    = "D" + str_volt + "V"
        self.instrument.write( str_command )   #Voltage Source Command
        #str_status      = self.instrument.query('V?')   # V3,V4,V5,V6
        #print("Set Voltage Status = ", str_status )
        # End Advantest R6243 
        return
    
    # Current Source Command
    def Set_Current(self,current):
        str_current = str(current)
        str_command    = "D" + str_current + "MA"
        self.instrument.write( str_command )   #Current Source Command
        # End Advantest R6243 
        return
    
    # Read input
    def Read_input(self):
        str_status      = self.instrument.query('D?')
        #print("Read_input Status = ", str_status )         # D+1.0000E+0V,D 2.0000E+0A
        str_status_0    = str_status.split(',', 1)[0]       #  ←','で2分割、インデックス番号0番を取り出す
        str_status_1    = str_status.split(',', 1)[1]       #  ←','で2分割、インデックス番号1番を取り出す
        value           = float( str_status_0[1:11] )
        unit            = str_status_0[11:12]
        value1_limit    = float( str_status_1[1:11] )
        unit1           = str_status_1[11:12]
        #print("Set Source Value = ", value, "Unit = ", unit )
        # End Advantest R6243 
        return value,unit,value1_limit,unit1
    
    # Read measured
    def Read(self):
        self.instrument.write('OM1')
        str_status      = self.instrument.read()  
        #print("Read Status = ", str_status )
        value           = float( str_status[4:] ) # 'DI +0.00023E+0'
        function        = str_status[1:2]
        #print("Read Value = ", value, "Function = ", function )
        # End Advantest R6243 
        return  value,function
    
    # Operate
    def Operate(self):
        self.instrument.write( 'E' )                    # E:Operated, H:Stand by
        # End Advantest R6243 
        return
    
    # Stand by
    def Stand_by(self):
        self.instrument.write( 'H' )                    # E:Operated, H:Stand by
        # End Advantest R6243 
        return
    
    # Operate_Status
    def Operate_Status(self):
        str_status      = self.instrument.query('E?')   # E:Operated, H:Stand by,  and return :'H\r\n'
        str_status_0    = str_status[:1]                #cut '\r\n'
        # print("Operate_Status = ", str_status )
        # dictionary
        dictionary = {'E' : 'Operated' , 'H' : 'Stand by'  }
        str_status_n = dictionary[str_status_0]
        print("Source Function Status = ", str_status_n )
        # End Advantest R6243 
        return
    
    def GoToLocal(self):
        self.rm.close()
        return
    
    # ID number query
    def ID_Number(self):
        str_ID_0    = self.instrument.query('*IDN?')    # ADVANTEST,R6243 ,10203548,B02\r\n
        str_ID      = str_ID_0.split('\r\n', 1)[0]      #  ←'\r\n'で2分割、インデックス番号0番を取り出す #cut '\r\n'
        #print("query *IDN? = ",str_ID )
        return str_ID
    
if __name__ == '__main__':
    Advantest_6243 = Application()
'''
    Advantest_6243.Stand_by()
    Advantest_6243.Operate()
    #Advantest_6243.Read_m()
    Advantest_6243.Operate_Status()
    
    current_limit = 2000.0     #(mA)
    Advantest_6243.Set_Current_Limit(current_limit)
    
    volt_in = 1.00
    print("input voltage = ", volt_in)
    Advantest_6243.Set_Voltage(volt_in)

    value,unit,value1_limit,unit1 = Advantest_6243.Read_input()
    print("Reprint \n Source Function = ",value," unit  = ",unit,", limit = ",value1_limit," unit  = ",unit1)

    value,function = Advantest_6243.Read()
    print("Reprint2 \n Measured = ",value," Measured Function = ", function)

    str_ID = Advantest_6243.ID_Number()
    print("query *IDN? = ",str_ID )

    volt_in = 0.00
    print("input voltage = ", volt_in)
    Advantest_6243.Set_Voltage(volt_in)

    Advantest_6243.Stand_by()
    Advantest_6243.Operate_Status()

    #Advantest_6243.GoToLocal()
'''
# usage example
# import Agilent34410A_read_module
#         self.Agilent34410A    = Agilent34410A_read_module.Application()
#         value  = self.Agilent34410A.Measure()
#         str_ID = self.Agilent34410A.ID_Number() 