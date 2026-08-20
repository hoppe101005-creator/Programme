from ctypes import *
from controler import controler

end_position_lose = 0
end_position_gespannt = 0
position_werkstück_wechsel = 0
position_speichern =False
spannen = True
loesen = False

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
    controler.nse_zu_position_bewegen(end_position_lose)
    print("gelöst")



            


