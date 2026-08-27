from ctypes import *
from controler import controler
import time
from sensor import sensor
import threading

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
        self.programmablauf_gestartet = False
        self.error_code = self.controler1.error_code
        self.kistler = sensor(ip="192.168.6.4",rack=0, slot=1, db_nummer=31, sensoradresse=0)

        self.controler1.geschwindigkeit = 0
        self.controler1.beschleunigung = 0
        self.controler1.verzoegerung = 0
    
        
        offen_wechsel = 8
        wechsel_gespannt = 30
        gespannt_geschlossen = 71 - offen_wechsel - wechsel_gespannt
        
        self.u_fakt = None
        self.offen = (0, -offen_wechsel, -offen_wechsel - wechsel_gespannt, -offen_wechsel - wechsel_gespannt - gespannt_geschlossen)
        self.wechsel = (offen_wechsel, 0, -wechsel_gespannt, -wechsel_gespannt-gespannt_geschlossen)
        self.gespannt = (offen_wechsel + wechsel_gespannt, wechsel_gespannt, 0 , -gespannt_geschlossen)
        self.geschlossen = (offen_wechsel + wechsel_gespannt + gespannt_geschlossen, wechsel_gespannt + gespannt_geschlossen, gespannt_geschlossen, 0)
        

    def programmablauf(self,motor,lage_motor, fahren, geschwindigkeit, beschleunigung, verzoegerung):

        if motor == "ACT":
            self.u_fakt = 12
        elif motor == "DeltaLine" or motor == "Maxon":
            self.u_fakt = 24
        elif motor == "Faulhaber":
            self.u_fakt == 21
            
        if lage_motor == "Offen":
            self.lage_motor = self.offen
        elif lage_motor == "Wechsel":
            self.lage_motor = self.wechsel
        elif lage_motor == "Gespannt":
            self.lage_motor = self.gespannt
        elif lage_motor == "Geschlossen":
            self.lage_motor = self.geschlossen

        loesen = False
        if fahren == "Geschlossen":
            print("Handle Programm:", self.handle)
            print("Handle Controller:", self.controler1.handle)
            print("Identisch:", self.handle == self.controler1.handle)
            self.controler1.nse_zu_position_bewegen(self.lage_motor[3]*self.u_fakt, geschwindigkeit, beschleunigung, verzoegerung)
            print("geschlossen")
            time.sleep(2)
        if fahren == "Gespannt":
            print("Messthread gestartet")
            print("Handle Programm:", self.handle)
            print("Handle Controller:", self.controler1.handle)
            print("Identisch:", self.handle == self.controler1.handle)
            self.controler1.nse_zu_position_bewegen(self.lage_motor[2]*self.u_fakt, geschwindigkeit, beschleunigung, verzoegerung)
            print("gespannt")
            self.kistler.mess_ablauf()
            loesen = True
            self.kistler.messung_abgeschlossen = False
        if fahren == "Wechsel" or loesen:
            print("Handle Programm:", self.handle)
            print("Handle Controller:", self.controler1.handle)
            print("Identisch:", self.handle == self.controler1.handle)
            self.controler1.nse_zu_position_bewegen(self.lage_motor[1]*self.u_fakt, geschwindigkeit, beschleunigung, verzoegerung)
            print("wechsel")
            time.sleep(2)
        if fahren == "Offen":
            print("Handle Programm:", self.handle)
            print("Handle Controller:", self.controler1.handle)
            print("Identisch:", self.handle == self.controler1.handle)
            self.controler1.nse_zu_position_bewegen(self.lage_motor[0]*self.u_fakt, geschwindigkeit, beschleunigung, verzoegerung)
            print("offen")
            time.sleep(2)
                            
        self.programmablauf_gestartet = True
                
                
    def get_drehzahl(self):        
        return self.controler1.aktuelle_drehzahl_auslesen() 
    

