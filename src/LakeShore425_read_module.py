import tkinter as tk
#from tkinter import ttk
from lakeshore import Model425      # see https://lake-shore-python-driver.readthedocs.io/en/latest/model_425.html

class Application:
    def __init__(self):
        try:
            #　計測機器(USB)
            self.my_instrument = Model425()
            str_text = 'UNIT ' + str(1)                             #set Feild_Unit_value into 'Gauss'
            self.my_instrument.command(str_text)
            str_text = 'RANGE ' + str(4)                            #set Feild_Range_value into 'Highest(±35.000 kG)'
            self.my_instrument.command(str_text)
        except:
            print('Error: LakeShore 425(USB) not Found ')

    # Measure 
    def Measure(self):

        # Feild_Unit
        Feild_Unit_module = ('No Change', 'Gauss', 'Tesla', 'Orsted', 'Ampere/meter')
        Feild_Unit_v = tk.StringVar()

        #str_ID    = self.my_instrument.query('*IDN?')      # Delete this line for speedup
        str_Value = self.my_instrument.query('RDGFIELD?')
        value     = float(str_Value)
        #str_Unit  = self.my_instrument.query('UNIT?')      # Delete this line for speedup
        #unit_tuple = Feild_Unit_module[ int(str_Unit) ]    # Delete this line for speedup
        unit_tuple = 'Gauss'                                # Add    this line for speedup
        #print("Value = ",value,",Unit = ",unit_tuple)

        return value,unit_tuple
    
    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        return str_ID


if __name__ == '__main__':
    root=tk.Tk()
    LS425 = Application()

    # value , unit = LS425.Measure() 
    # print("Reprint \n Value = ",value,",Unit = ",unit)
    
    #Gaussmeter.Measure()

# usage example
# import LakeShore425_read_module
#         self.LS425 = LakeShore425_read_module.Application()
#         value , unit    = self.LS425.Measure() 