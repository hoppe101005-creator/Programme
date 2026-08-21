from ctypes import *
from controler import controler
from abfragen import abfragen
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

controler = controler()
abfragen = abfragen()
lage_motor = abfragen.frage_motor_lage()
print (lage_motor)
gespeicherte_Werte_einlesen = True          ### Abfrage, ob gespeicherte Werte eingelesen werden sollen

position_speichern = False                  ### Abfrage, ob die aktuelle Position gespeichert werden soll
schliessen = False                          ### Abfrage, ob das NSE ganz schließen soll soll
spannen = True                             ### Abfrage, ob das NSE in Spannposition fahren soll
werkstück = True                          ### Abfrage, ob das NSE in Wechselposition fahren soll
loesen = False                               ### Abfrage, ob das NSE ganz öffnen soll

controler.geschwindigkeit = 1500             ### Eingabe der Drehzahl
controler.beschleunigung = 10000             ### Eingabe der Beschleunigung
controler.verzögerung = 500                  ### Eingabe der Verzögerung

handle = controler.open_device()

for i in range(20):
    if gespeicherte_Werte_einlesen:
        controler.end_position_lose = lage_motor[0]
        controler.end_position_gespannt = lage_motor[2]
        controler.position_werkstück_wechsel = lage_motor[1]
        controler.position_geschlossen = lage_motor[3]
        print("Endposition lose: ", controler.end_position_lose)
        print("Endposition gespannt: ", controler.end_position_gespannt)
        aktuelle_position = controler.aktuelle_position_auslesen()

    if position_speichern:
        controler.position_speichern("end_position_gespannt.txt",aktuelle_position)
    if schliessen:
        controler.nse_zu_position_bewegen(controler.position_geschlossen)
        print("geschlossen")
        time.sleep(2)
    if spannen:
        controler.nse_zu_position_bewegen(controler.end_position_gespannt)
        print("gespannt")
        time.sleep(2)
    if werkstück:
        controler.nse_zu_position_bewegen(controler.position_werkstück_wechsel)
        print("wechsel")
        time.sleep(2)
    if loesen:
        controler.nse_zu_position_bewegen(controler.end_position_lose)
        print("gelöst")
        time.sleep(2)
                    