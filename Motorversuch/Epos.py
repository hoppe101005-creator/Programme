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
        self.controler = controler()        

        self.controler.geschwindigkeit = 0
        self.controler.beschleunigung = 0
        self.controler.verzoegerung = 0
        
        self.act_offen = (0,-100,-840,-850)
        self.act_wechsel = (100, 0, -740, -750)
        self.act_gespannt = (840, 740, 0, -10)
        self.act_geschlossen = (850, 750, 10, 0)
        

    def programmablauf(self,motor,lage_motor, fahren, geschwindigkeit, beschleunigung, verzoegerung):
        self.handle = self.controler.open_device()
        
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
                self.controler.nse_zu_position_bewegen(self.lage_motor[3], geschwindigkeit, beschleunigung, verzoegerung)
                print("geschlossen")
                time.sleep(2)
            if fahren == "Gespannt":
                self.controler.nse_zu_position_bewegen(self.lage_motor[2], geschwindigkeit, beschleunigung, verzoegerung)
                print("gespannt")
                time.sleep(2)
            if fahren == "Wechsel":
                self.controler.nse_zu_position_bewegen(self.lage_motor[1], geschwindigkeit, beschleunigung, verzoegerung)
                print("wechsel")
                time.sleep(2)
            if fahren == "Offen":
                self.controler.nse_zu_position_bewegen(self.lage_motor[0], geschwindigkeit, beschleunigung, verzoegerung)
                print("offen")
                time.sleep(2)
                
            
                
    
"""    def gespeicherte_werte_einlesen():
        self.controler.end_position_lose = self.lage_motor[0]
        self.controler.end_position_gespannt = self.lage_motor[2]
        self.controler.position_werkstück_wechsel = self.lage_motor[1]
        self.controler.position_geschlossen = self.lage_motor[3]
        print("Endposition lose: ", self.controler.end_position_lose)
        print("Endposition gespannt: ", self.controler.end_position_gespannt)
        self.aktuelle_position = self.controler.aktuelle_position_auslesen()
        
        if position_speichern:
            self.controler.position_speichern("end_position_gespannt.txt",aktuelle_position)
                
        """