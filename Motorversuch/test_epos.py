from ctypes import *
from controler import controler

end_position_lose = 0
end_position_gespannt = 0
position_werkstück_wechsel = 0
position_speichern =False
spannen = False
loesen = True
error_code = c_uint(0)
node_id = 1

controler = controler()

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS2\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = WinDLL(dll_path)
handle = controler.open_device()

end_position_lose = controler.position_einlesen("end_position_lose.txt")
end_position_gespannt = controler.position_einlesen("end_position_gespannt.txt")

print("Endposition lose: ", end_position_lose)
print("Endposition gespannt: ", end_position_gespannt)
aktuelle_position = controler.aktuelle_position_auslesen()

controler.nse_zu_position_bewegen(end_position_lose)
            
epos.VCS_ActivateProfilePositionMode(
    handle,
    node_id,
    byref(error_code)
    ) 
       
epos.VCS_MoveToPosition(
    handle,
    node_id,
    end_position_lose,
    1,
    1,
    byref(error_code))

enabled = c_int()

epos.VCS_GetEnableState(
    handle,
    node_id,
    byref(enabled),
    byref(error_code)
)

print(enabled.value)