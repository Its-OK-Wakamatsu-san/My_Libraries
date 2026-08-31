import thorlabs_apt as apt      
# see read.me  https://github.com/qpit/thorlabs_apt
# see APT.DLL wrapper  https://github.com/qpit/thorlabs_apt/blob/master/thorlabs_apt/_APTAPI.py  
# see apt.method https://github.com/qpit/thorlabs_apt/blob/master/thorlabs_apt/core.py 
import time

class Application:
    def __init__(self):
        
        # Assign TDC001
        try:
            #check ID and serial No.
            tuple=()
            tuple=apt.list_available_devices()
            print(tuple)
            #[(31, 83815209)]                   # TDC001 Production ID=31 Production Serial Number=83815209
            # Assign TDC001
            ID = self.ID = int(tuple[0][0])           #  ID
            SN= self.SN = int(tuple[0][1])           #  SN
            print (ID,SN)
            self.apt_TDC001 = apt.Motor(SN)     # TDC001 Production ID=31 Production Serial Number=83815209
        except:
            print("missing Motor!")

    # Not use apt_TDC001.move_to(210.)  
    # Up Command that crosses 180 like as 175->210 is move not correct
    # (Move down175->0->-150). Replaced below.
    def Move_Abs(self,set_position):
        present_position = self.apt_TDC001.position      # check PP
        diff = set_position - present_position
        if   diff < -180.0:
            diff +=  360.0
        elif diff >  180.0:
            diff -=  360.0

        # set wait time
        if   abs(diff) > 40.0:
            wait_time = 40.0
        elif abs(diff) > 10.0:
            wait_time = 15.0
        elif abs(diff) > 0.5:
            wait_time = 6.0
        else:
            wait_time = 4.0

        self.apt_TDC001.move_by(diff) 
        time.sleep(wait_time)
        present_position = self.apt_TDC001.position 
        return present_position
    
    def Move_Rel(self,diff):
        self.apt_TDC001.move_by(diff)   # diff<0.5deg, then sleep time=4.0sec
        time.sleep(4.0)                 # diff<0.5deg, then sleep time=4.0sec
        present_position = self.apt_TDC001.position    # check PP
        return present_position
    
    def Move_Home(self):
        self.apt_TDC001.move_home(True)
        present_position = self.apt_TDC001.position    # check PP
        return present_position

    def P_P(self):                                      #present_position
        time.sleep(0.1)
        present_position = self.apt_TDC001.position    # check PP
        return present_position
    
    def Jog_P01(self):                                  #Jog 0.1deg
        time.sleep(0.1)
        self.apt_TDC001.move_by(0.1) 
        time.sleep(4.0)            
        present_position = self.apt_TDC001.position     # check PP
        return present_position
    
    def Jog_N01(self):                                  #Jog -0.1deg
        self.apt_TDC001.move_by(-0.1)   
        time.sleep(4.0)             
        present_position = self.apt_TDC001.position     # check PP
        return present_position

    def Jog_P05(self):                                  #Jog 0.5deg
        self.apt_TDC001.move_by(0.5)   
        time.sleep(4.0)             
        present_position = self.apt_TDC001.position     # check PP
        return present_position
    
    def Jog_N05(self):                                  #Jog -0.5deg
        self.apt_TDC001.move_by(-0.5)   
        time.sleep(4.0)             
        present_position = self.apt_TDC001.position     # check PP
        return present_position
    
    def ID_Number(self):                                #ID
        return self.ID,self.SN
    
    
if __name__ == '__main__':
    TDC001 = Application()
'''        
    pp = TDC001.Move_Abs(5.0)
    print(pp)
    pp = TDC001.Move_Rel(-0.3)
    print(pp)
    pp = TDC001.Move_Home()
    print(pp)
    pp = TDC001.P_P()
    print(pp)
    pp = TDC001.Jog_P05()
    print(pp)
    pp = TDC001.Jog_P01()
    print(pp)
    pp = TDC001.Jog_N05()
    print(pp)
    pp = TDC001.Jog_N01()
    print(pp)
'''

# usage example
# import ThorLABS_TDC001_module
#         self.TDC001       = ThorLABS_TDC001_module.Application()
#         Present_Position  = self.TDC001.Jog_P05()
