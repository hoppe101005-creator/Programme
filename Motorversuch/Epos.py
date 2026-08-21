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

controler = controler()

controler.position_geschlossen = 0                    ### Position, an der das NSE komplett geschlossen ist
controler.end_position_lose = 0                       ### Position, an der das NSE komplett geöffnet ist
controler.end_position_gespannt = 0                   ### Position, an der das NSE spannt
controler.position_werkstück_wechsel = 0              ### Position, an der ein neues Teil eingelegt werden kann


gespeicherte_Werte_einlesen = True          ### Abfrage, ob gespeicherte Werte eingelesen werden sollen

position_speichern = False                  ### Abfrage, ob die aktuelle Position gespeichert werden soll
schliessen = False                          ### Abfrage, ob das NSE ganz schließen soll soll
spannen = True                              ### Abfrage, ob das NSE in Spannposition fahren soll
werkstück = False                           ### Abfrage, ob das NSE in Wechselposition fahren soll
loesen = True                               ### Abfrage, ob das NSE ganz öffnen soll

controler.geschwindigkeit = 1500             ### Eingabe der Drehzahl
controler.beschleunigung = 10000             ### Eingabe der Beschleunigung
controler.verzögerung = 500                  ### Eingabe der Verzögerung

handle = controler.open_device()

for i in range(1):
    if gespeicherte_Werte_einlesen:
        controler.end_position_lose = controler.position_einlesen("end_position_lose.txt")
        controler.end_position_gespannt = controler.position_einlesen("end_position_gespannt.txt")
        controler.position_werkstück_wechsel = controler.position_einlesen("position_werkstück_wechsel.txt")
        controler.position_geschlossen = controler.position_einlesen("position_geschlossen.txt")
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
