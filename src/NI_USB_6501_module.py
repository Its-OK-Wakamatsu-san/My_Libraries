# https://github.com/ni/nidaqmx-python/blob/master/examples/digital_in/read_dig_lines.py
import nidaqmx
from nidaqmx.system import System
from nidaqmx.constants import LineGrouping
import warnings
import time

class Application:
    def __init__(self, device_name="Dev1"):
        self.device_name = device_name
        devices = [d.name for d in System.local().devices]
        if self.device_name not in devices:
            warnings.warn(f"デバイス '{self.device_name}' が見つかりません。利用可能なデバイス: {devices}")
    
    def Get_Pin_Direction(self, line):
        """
        指定したデジタルラインが入力モードか出力モードかを推定します。
        NI-DAQmx APIでは直接ピンのモードを取得できないため、タスク作成時の例外で判定します。
        戻り値: "input", "output", または "unknown"
        """
        try:
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan(f"{self.device_name}/{line}")
                return "output"
        except nidaqmx.DaqError:
            try:
                with nidaqmx.Task() as task:
                    task.di_channels.add_di_chan(f"{self.device_name}/{line}")
                    return "input"
            except nidaqmx.DaqError:
                return "unknown"
            
    def Properties (self):   
        local_system = nidaqmx.system.System.local()
        driver_version = local_system.driver_version
        str_comment  = str("DAQmx {}.{}.{}".format(
            driver_version.major_version,
            driver_version.minor_version,
            driver_version.update_version) )+ '\n'
        for device in local_system.devices:
            str_comment  +=  str("Device Name: {}, Product Category: {}, Product Type: {}".format(
                device.name, device.product_category, device.product_type)) + '\n'
        return str_comment

    def Disconnect(self):
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan("Dev1/port0/line0:7", line_grouping=LineGrouping.CHAN_PER_LINE)
            task.do_channels.add_do_chan("Dev1/port1/line0:7", line_grouping=LineGrouping.CHAN_PER_LINE)
            task.do_channels.add_do_chan("Dev1/port2/line0:7", line_grouping=LineGrouping.CHAN_PER_LINE)
            task.stop()
            # 明示的に出力チャンネルとして設定
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan("Dev1/port0/line0")
            task.stop()
        return 
    
    def Write_Digital_Pin(self, line, value):

        with nidaqmx.Task() as task:
            # 明示的に出力チャンネルとして設定
            task.do_channels.add_do_chan(f"{self.device_name}/{line}")
            task.write(value)
        return
 
    def Read_Digital_Pin(self, line):
        """
        指定したデジタル入力ラインから値を読み込みます。
        line: 例 "port0/line0"
        戻り値: True または False
        readがうまくいかない。
        """
        with nidaqmx.Task() as task:
            task.di_channels.add_di_chan(f"{self.device_name}/{line}")
            return task.read()
        

# 使用例
if __name__ == "__main__":
    usb6501 = Application("Dev1")

    # port0～port2の全ピンの入出力モードを表示
    print("USB-6501のピンの入出力モードを確認します。")
    for port in range(3):
        for line in range(8):
            pin = f"port{port}/line{line}"
            direction = usb6501.Get_Pin_Direction(pin)
            print(f"{pin}: {direction}")

    # デジタル出力ピンに値を書き込みます。
    usb6501.Write_Digital_Pin("port0/line0", True)
    usb6501.Write_Digital_Pin("port1/line0", True)
    time.sleep(1)  # 1秒待機
    str_read = usb6501.Read_Digital_Pin("port0/line0")
    print(f"port0/line0の読み取り値: {str_read}") 
    str_read = usb6501.Read_Digital_Pin("port1/line0")
    print(f"port1/line0の読み取り値: {str_read}")
    time.sleep(1)  # 1秒待機

    usb6501.Write_Digital_Pin("port0/line0", False)
    usb6501.Write_Digital_Pin("port1/line0", False) 
    time.sleep(1)  # 1秒待機
    str_read = usb6501.Read_Digital_Pin("port0/line0")
    print(f"port0/line0の読み取り値: {str_read}")
    str_read = usb6501.Read_Digital_Pin("port1/line0")
    print(f"port1/line0の読み取り値: {str_read}")

    #　readがうまくいかない。
    usb6501.Disconnect()
    print("USB-6501の接続を解除しました。")