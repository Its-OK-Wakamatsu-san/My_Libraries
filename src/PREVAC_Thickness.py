import numpy as np

#PREVAC TM14, thickness calculation from LabVIEW Math Script Module.

class LabVIEW_Application:
    def Thickness(self,thickness_cluster):
        FFilmDensity        = thickness_cluster[0]
        FAcousticImpedance  = thickness_cluster[1]
        AFreqMin            = thickness_cluster[2]
        AFreqMax            = thickness_cluster[3]
        tooling             = thickness_cluster[4]
        
        AConstans =((1.68E13*2.648)/(np.pi*8.83))*(FAcousticImpedance/FFilmDensity)
        tg1=np.tan(((6000000) - AFreqMax)/(6000000.0/np.pi))
        tg2 = np.tan(((6000000) - AFreqMin)/(6000000.0/np.pi))
        arctg1 = np.atan2((8.83*tg1),FAcousticImpedance)
        arctg2 = np.atan2((8.83*tg2),FAcousticImpedance)
        Thickness = ( (AConstans*((arctg1/AFreqMax)-(arctg2/AFreqMin)) ) *tooling) / 100.0
        Thickness =-Thickness           #unit Ångström ... 0.1nm 100pm

        return Thickness
    
if __name__ == '__main__':
    PREVAC = LabVIEW_Application()

    #thickness_cluster = []
    #PREVAC.Thickness()

