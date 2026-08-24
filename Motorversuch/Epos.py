from ctypes import *
from controler import controler
import time

"""850 Schritte zwischen anfangs und endlage"""
"""..........................."""
"""                           """
"""       |   Auf   |   Zu    """
"""  ACT  |    +    |    -    """
"""  Fau  |    -    |    +    """
"""  MAX  |    +    |    -    """
"""..........................."""

"""     Abstände der Anschläge:          """
"""     geschlossen -> gespannt: 10      """
"""     geschlossen -> wechsel:  750     """
"""     geschlossen -> offen:    850     """
"""                                      """

class epos():
    def __init__(self):
        self.controler1 = controler() 
        self.handle = self.controler1.open_device()
        self.drehzahl = None

        self.controler1.geschwindigkeit = 0
        self.controler1.beschleunigung = 0
        self.controler1.verzoegerung = 0
        
        self.act_offen = (0,-100,-840,-850)
        self.act_wechsel = (100, 0, -740, -750)
        self.act_gespannt = (840, 740, 0, -10)
        self.act_geschlossen = (850, 750, 10, 0)
        

    def programmablauf(self,motor,lage_motor, fahren, geschwindigkeit, beschleunigung, verzoegerung):
   
        if motor == "ACT":
            if lage_motor == "Offen":
                self.lage_motor = self.act_offen
            elif lage_motor == "Wechsel":
                self.lage_motor = self.act_wechsel
            elif lage_motor == "Gespannt":
                self.lage_motor = self.act_gespannt
            elif lage_motor == "Geschlossen":
                self.lage_motor = self.act_geschlossen

            if fahren == "Geschlossen":
                print("Handle Programm:", self.handle)
                print("Handle Controller:", self.controler1.handle)
                print("Identisch:", self.handle == self.controler1.handle)
                self.controler1.nse_zu_position_bewegen(self.lage_motor[3], geschwindigkeit, beschleunigung, verzoegerung)
                print("geschlossen")
                time.sleep(2)
            if fahren == "Gespannt":
                print("Handle Programm:", self.handle)
                print("Handle Controller:", self.controler1.handle)
                print("Identisch:", self.handle == self.controler1.handle)
                self.controler1.nse_zu_position_bewegen(self.lage_motor[2], geschwindigkeit, beschleunigung, verzoegerung)
                print("gespannt")
                time.sleep(2)
            if fahren == "Wechsel":
                print("Handle Programm:", self.handle)
                print("Handle Controller:", self.controler1.handle)
                print("Identisch:", self.handle == self.controler1.handle)
                self.controler1.nse_zu_position_bewegen(self.lage_motor[1], geschwindigkeit, beschleunigung, verzoegerung)
                print("wechsel")
                time.sleep(2)
            if fahren == "Offen":
                print("Handle Programm:", self.handle)
                print("Handle Controller:", self.controler1.handle)
                print("Identisch:", self.handle == self.controler1.handle)
                self.controler1.nse_zu_position_bewegen(self.lage_motor[0], geschwindigkeit, beschleunigung, verzoegerung)
                print("offen")
                time.sleep(2)
                
    def get_drehzahl(self):        
        return self.controler1.aktuelle_drehzahl_auslesen() 
    
