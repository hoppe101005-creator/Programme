"""ACT Abstand zwischen Positionen"""
ACT_offen_wechsel = 60
ACT_offen_spannen = 830
ACT_offen_geschlossen = 850

"""ACT Absolutwerte der Positionen, jeh nach Ausgangslage des NSE"""
ACT_Offen = (0, -ACT_offen_wechsel, -ACT_offen_spannen, -ACT_offen_geschlossen)
ACT_Wechsel = (ACT_offen_wechsel, 0, -ACT_offen_spannen + ACT_offen_wechsel, -ACT_offen_geschlossen + ACT_offen_wechsel)
ACT_Spannen = (ACT_offen_spannen, ACT_offen_spannen - ACT_offen_wechsel, 0, )
ACT_Geschlossen = (ACT_offen_geschlossen, ACT_offen_geschlossen -ACT_offen_wechsel, ACT_offen_geschlossen - ACT_offen_spannen, 0)


class abfragen():
    def __init__(self):
        self.absolute_position = tuple
    
    def frage_motor_lage(self):
        eingabe = False
        while not eingabe:
            eingabe = True
            print("Eingabemöglichkeiten Frage 1: A = ACT, D = DeltaLine, F = Faulhaber, M = Maxon")
            print("Eingabemöglichkeiten Frage 2: O = Offen, W = Wechsel, S = Spannen, G = Geschlossen")
            motor = input ("Welcer Motor soll getestet werden? (A/D/F/M)")
            lage = input ("In welcher Lage befindet sich das NSE? (O/W/S/G)")
            print("Motor: ",motor)
            print("Lage: ",lage)
            if motor == "A":
                if lage == "O":
                    self.absolute_position = ACT_Offen
                elif lage == "W":
                    self.absolute_position = ACT_Wechsel
                elif lage == "S":
                    self.absolute_position = ACT_Spannen
                elif lage == "G":
                    self.absolute_position = ACT_Geschlossen
                else:
                    eingabe = False
                    print("falsche Eingabe")
        return self.absolute_position
    
    def bool_setzen(self, frage):
        eingabe = False
        while not eingabe:
            antwort =input(frage + "(Ja/Nein)")
            if antwort == "Ja" or antwort =="ja":
                eingabe = True
                return True
            if antwort == "Nein" or antwort == "nein":
                eingabe = True
                return False
            else:
                print ("Falsche Eingabe")
    
    def frage_int(self, frage):
         eingabe = False
         while not eingabe:
            antwort =int(input(frage + "(Nennen sie eine Zahl)"))
            if type(antwort) == int:
                return antwort
            else:
                print ("Falsche Eingabe")