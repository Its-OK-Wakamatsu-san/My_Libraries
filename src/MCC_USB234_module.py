# Command           https://files.digilent.com/manuals/Mcculw_WebHelp/ULStart.htm
# Connect Device    https://github.com/mccdaq/mcculw/blob/master/examples/console/a_in.py
# Analog in         https://github.com/mccdaq/mcculw/blob/master/examples/console/v_in.py
# Analog Output     https://github.com/mccdaq/mcculw/blob/master/examples/console/v_out.py
from mcculw import ul
from mcculw.enums import InterfaceType
from mcculw.device_info import DaqDeviceInfo
import time

class Application:
    def __init__(self):
        self.device = None
        self.board_num = 0
        self.daq_dev_info = None
        self.ao_channel = 0     # D/A OUT 0
        self.ao_range = None
        self.ao_info = None
        self.ao_min_interval = 1/50  # sec
        self.ai_channel = 0     # CH0 IN
        self.ai_range = None
        self.ai_info = None
        self.adc_ready = False
        self.input_mode = 1     # single-ended mode
        self.Connect_Device()

    def Connect_Device(self):
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.USB)
        if not devices:
            raise Exception('Error: No DAQ devices found')
        print('Found', len(devices), 'DAQ device(s):')
        self.device = devices[0]
        try:
            ul.create_daq_device(self.board_num, self.device)
            self.daq_dev_info = DaqDeviceInfo(self.board_num)
            if not self.daq_dev_info.supports_analog_output:
                raise Exception('Error: The DAQ device does not support analog output')
            print('\nActive DAQ device: ', self.daq_dev_info.product_name, ' (',self.daq_dev_info.unique_id, ')\n', sep='')
            self.ao_info = self.daq_dev_info.get_ao_info()
            self.ao_range = self.ao_info.supported_ranges[0]
            self.ai_info = self.daq_dev_info.get_ai_info()
            self.ai_range = self.ai_info.supported_ranges[0]
            print(' self.ao_info = ',self.ao_info,'\n self.ao.range = ',self.ao_range,'\n self.ao_info = ',
                                     self.ao_info,'\n self.ai_range',self.ai_range )
            self.adc_ready = True                                               # MCC_USB234 Ready
            ul.a_input_mode(self.board_num, self.input_mode)
            ul.v_out(self.board_num, self.ao_channel, self.ao_range, 0)
        except Exception as e:
            print('\n', e)
        return
    
    # Analog_in  -> Digital_in
    def Get_Voltage(self, assign_channel):
        self.ai_channel = assign_channel
        #print('self.board_num, self.ai_channel, self.ai_range = ' , self.board_num, self.ai_channel, self.ai_range)
        if self.adc_ready:
            try:
                if self.ai_info.resolution <= 16:
                    # Get a value from the device
                    value = ul.a_in(self.board_num, self.ai_channel, self.ai_range)
                    # Convert the raw value to engineering units
                    #print('ID, value=',self.ai_channel,value)
                    eng_units_value = ul.to_eng_units(self.board_num, self.ai_range, value)
                else:
                    value = ul.a_in_32(self.board_num, self.ai_channel, self.ai_range)
                    eng_units_value = ul.to_eng_units_32(self.board_num, self.ai_range, value)
                return eng_units_value
            except Exception as e:
                print('\n', e)
                self.adc_ready = False
        else:
            print("DAQ device is not ready")
            return
        
    #  Digital_out -> Analog_out
    def Set_Voltage(self,  assign_channel , value ):
        self.ao_channel = assign_channel
        if self.adc_ready:
            try:
                ul.v_out(self.board_num, self.ao_channel, self.ao_range, value)   # 出力
            except Exception as e:
                self.adc_ready = False
                print('\n', e)
        else:
            print("DAQ device is not ready")
            return
        
    def Disconnect_Device(self):
        ul.release_daq_device(self.board_num)
        return

if __name__ == '__main__':
    USB234 = Application()

    v0=USB234.Get_Voltage(0)
    v1=USB234.Get_Voltage(1)
    v2=USB234.Get_Voltage(2)
    v4=USB234.Get_Voltage(4)
    v5=USB234.Get_Voltage(5)
    v6=USB234.Get_Voltage(6)
    v7=USB234.Get_Voltage(7)
    print(' Voltage(kV)        = ',v0,'\n','Current            = ',v1)
    print(' +Vcc(10V)          = ',v2)
    print(' High:interlocks On = ',v4,'\n','Low:interlocks On  = ',v5)
    print(' High Voltage On    = ',v6,'\n','Source Current On  = ',v7)
    USB234.Set_Voltage( 0 , 0.1 )
    time.sleep(0.5)
    v0=USB234.Get_Voltage(0)
    print(' Voltage(kV)        = ',v0)    
    USB234.Set_Voltage( 0 , 0.0 )
    time.sleep(3.0)
    v0=USB234.Get_Voltage(0)
    print(' Voltage(kV)        = ',v0)  
    # usage example
    # import MCC_USB234_module
    #         self.USB234   = MCC_USB234_module.Application()
    #         usb234_chan_0 = self.USB234.Get_Voltage(channel_0)
