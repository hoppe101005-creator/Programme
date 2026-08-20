from ctypes import *
from controler import controler

"""850 Schritte zwischen anfangs und endlage"""
""""""
"""       .   Auf   .   Zu    """
"""  ACT  .    +    .    -    """
"""  Fau  .    -    .    +    """
""""""

end_position_lose = 0
end_position_gespannt = 0
position_werkstück_wechsel = 0
position_speichern =False
spannen = False
werkstück = False
loesen = True

controler = controler()

handle = controler.open_device()

end_position_lose = controler.position_einlesen("end_position_lose.txt")
end_position_gespannt = controler.position_einlesen("end_position_gespannt.txt")

print("Endposition lose: ", end_position_lose)
print("Endposition gespannt: ", end_position_gespannt)
aktuelle_position = controler.aktuelle_position_auslesen()

if position_speichern:
    controler.position_speichern("end_position_gespannt.txt",aktuelle_position)
if spannen:
    controler.nse_zu_position_bewegen(end_position_gespannt)
    print("gespannt")
if loesen:
    controler.nse_zu_position_bewegen(position_werkstück_wechsel)
    print("wechsel")
if loesen:
    controler.nse_zu_position_bewegen(end_position_lose)
    print("gelöst")



            


