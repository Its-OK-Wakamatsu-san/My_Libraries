import pyvisa as visa

class Application:
    def __init__(self):
        try:
            #　計測機器と通信処置
            rm = visa.ResourceManager('@py')
            self.instrument = rm.open_resource('GPIB0::9::INSTR')
        except:
            print('Error: AP-1628T(GPIB address::9) not Found ')

    def Set_Pulse(self,pulse_target):    

        # 例外処置　-1の時　+65535が入力されるようなので、強制変更する
        if pulse_target == -1:
            pulse_target = -2
        '''
        if pulse_target > 32000:                # Max set
            pulse_target = 32000
        if pulse_target < -32000:
            pulse_target = -32000
        '''
        '''
            if pulse_target > 5500:             # for WS2.2-20SL-1100   Up to +/-22.2A
            pulse_target = 5500
        if pulse_target < -5500:
            pulse_target = -5500
        '''
        # Send Pulse Command
        pulse_now   =  pulse_target 
        str_text    = 'A1D' + str(pulse_now)
        self.instrument.write( str_text )
        return
    
    def Reply_Pulse(self):  
        self.instrument.write( 'T1')
        str_value       = self.instrument.read()                  #  ←AP-1628T 　読込み
        str_read        = str_value.split(',', 5)[0]              #  ←','で6分割、インデックス番号0番を取り出す
        pulse_reply      = float(str_read[3:])
        return pulse_reply

    #通信を切断する
    def Close_Instrument(self): 
        self.instrument.close()
        #rm.close()
        return

    # ID number query
    def ID_Number(self):
        str_ID = self.instrument.query('*IDN?')
        return str_ID

if __name__ == '__main__':
    AP1628T = Application()
    
    #pulse_read = AP1628T.Set_Pulse(0)
    #print("Reprint \n Pulse_read = ",pulse_read)

# usage example
# import AP1628T_CMD_module
#         self.TAKASAGO = AP1628T_CMD_module.Application()
#         pulse_read    = self.TAKASAGO.Set_Pulse(0) 