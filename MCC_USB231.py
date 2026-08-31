from mcculw import ul
from mcculw.enums import InterfaceType
from mcculw.device_info import DaqDeviceInfo
from matplotlib import pyplot as plt
import numpy as np
import time

class USB231:
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
        self.gain = 1.0        # 2022/12/21  add
        self.bias = 0.0003606622869321008    # 2022/12/21  add
        self.adc_ready = False
        self.input_mode = 1     # single-ended mode

    def initialize(self):
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.USB)
        if not devices:
            raise Exception('Error: No DAQ devices found')
        #time.sleep(5)
        print('Found', len(devices), 'DAQ device(s):')
        self.device = devices[0]
        try:
            ul.create_daq_device(self.board_num, self.device)
            self.daq_dev_info = DaqDeviceInfo(self.board_num)
            if not self.daq_dev_info.supports_analog_output:
                raise Exception('Error: The DAQ device does not support '
                                'analog output')
            print('\nActive DAQ device: ', self.daq_dev_info.product_name, ' (',
                  self.daq_dev_info.unique_id, ')\n', sep='')
            self.ao_info = self.daq_dev_info.get_ao_info()
            self.ao_range = self.ao_info.supported_ranges[0]
            self.ai_info = self.daq_dev_info.get_ai_info()
            self.ai_range = self.ai_info.supported_ranges[0]
            self.adc_ready = True
            ul.a_input_mode(self.board_num, self.input_mode)
            ul.v_out(self.board_num, self.ao_channel, self.ao_range, 0)
        except Exception as e:
            print('\n', e)


    #  GainやBiasを気にせずに出力する基礎関数
    def setVoltage(self, vol):
        if self.adc_ready:
            try:
                ul.v_out(self.board_num, self.ao_channel, self.ao_range, vol)   # 出力
            except Exception as e:
                self.adc_ready = False
                print('\n', e)
        else:
            return

    # 増幅されて出力している電圧を読み取る関数
    def getVoltage(self):
        if self.adc_ready:
            try:
                if self.ai_info.resolution <= 16:
                    # Get a value from the device
                    value = ul.a_in(self.board_num, self.ai_channel, self.ai_range)
                    # Convert the raw value to engineering units
                    eng_units_value = ul.to_eng_units(self.board_num, self.ai_range, value)
                else:
                    value = ul.a_in_32(self.board_num, self.ai_channel, self.ai_range)
                    eng_units_value = ul.to_eng_units_32(self.board_num, self.ai_range, value)
                return eng_units_value
            except Exception as e:
                print('\n', e)
                self.adc_ready = False
        else:
            print("ADC is not ready")
            return

    # 電圧を変更
    def setVoltageByThickStep(self, vol, step=1/30, interval=0.04):
        if self.adc_ready:
            v_current = self.toAttenuatedVoltage(self.getVoltage())     # 現在の出力電圧から現在の入力電圧を計算
            if v_current >= vol:        # 現在の入力電圧が設定する入力電圧より高い場合
                vols = np.flipud(np.arange(vol, v_current, step))       # 正から負に
            else:
                vols = np.arange(v_current, vol, step)      # 負から正に
            for v in vols:
                try:
                    self.setVoltage(v)
                    time.sleep(0.01)
                except Exception as e:
                    print('\n', e)
                    self.setVoltage(self.toAttenuatedVoltage(0))
                    return
            return
        else:
            return

    # 増幅後の出力電圧がvolになるように
    def setAmplifiedVoltageByThickStep(self, vol, step=1/50, interval=0.04):
        self.setVoltageByThickStep(vol=self.toAttenuatedVoltage(vol), step=step, interval=interval)
        return

    # 入力電圧から増幅後の出力電圧を計算
    def toAmplifiedVoltage(self, vol):
        return self.gain * vol + self.bias

    # 増幅後の電圧→入力電圧を計算
    def toAttenuatedVoltage(self, vol):
        return (vol - self.bias) / self.gain

    # 入力電圧の修正を行う
    def out_in_correction(self):
        print("out in voltage correction")
        if self.adc_ready:
            input_vols = []
            output_vols = []
            vols_ini = np.arange(0, -(self.ao_range.range_max-2), -0.2)
            #2022/12/21　change from -10V to +10V, 11 points
            vols = np.linspace(-(self.ao_range.range_max-0), (self.ao_range.range_max-0), 5)       # 入力電圧のリスト作成0Vから最大値まで20点 　
            for v_ini in vols_ini:
                self.setVoltage(v_ini)
                time.sleep(0.1)
            for v in vols:
                v_current = self.getVoltage()
                if (v_current > self.ai_range.range_max) or (v_current < -self.ai_range.range_max):
                    print(v_current, self.ai_range.range_max)
                    print('出力電圧が測定範囲外です')
                    return
                else:
                    self.setVoltage(v)
                    time.sleep(1.5)
                    vout = self.getVoltage()
                    print('Output: ' + str(vout) + ' V')
                    input_vols.append(vout)    # 増幅された電圧
                    output_vols.append([v, 1])  # ADCの出力電圧
            input_vols = np.array(input_vols)
            output_vols = np.array(output_vols)
            const = np.linalg.inv(output_vols.T @ output_vols) @ output_vols.T @ input_vols     # 回帰直線
            self.gain = const[0]        # 傾き
            self.bias = const[1]        # 切片
            print("Gain:" + str(self.gain) + ", Bias:" + str(self.bias))
            self.setAmplifiedVoltageByThickStep(0)  # 0Vに設定
            # plot
            plt.figure()
            plt.scatter(output_vols[:, 0], input_vols)
            x = np.linspace(-self.ao_range.range_max, self.ao_range.range_max, 5)
            y = self.gain * x + self.bias
            plt.plot(x, y)
            plt.xlabel("ADC output")
            plt.ylabel("Power output")
            plt.show()
            return
        else:
            print("ADC is not ready")
            return

    def degaussing(self, interval=200, step=60, alpha=0.05, beta=0.1, gamma=20):
        if self.adc_ready:
            try:
                v_start = self.toAttenuatedVoltage(self.getVoltage())
                steps = np.arange(0, 60, 1)
                for t in steps:
                    self.setVoltageByThickStep(
                        vol=v_start / 2 * np.exp(-alpha * t) * (np.cos((1 / (1 + np.exp(-beta * (t - gamma)))) * t)) + v_start / 2,
                        step=0.02
                    )
                    time.sleep(max(interval, self.ao_min_interval) / 1000)

                self.setVoltage(self.toAttenuatedVoltage(0))
                return
            except Exception as e:
                self.adc_ready = False
                print('\n', e)
        else:
            return

    def quit(self):
        ul.release_daq_device(self.board_num)


if __name__ == '__main__':
    adc = USB231()
    adc.initialize()
    adc.out_in_correction()

