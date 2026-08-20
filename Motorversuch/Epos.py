from ctypes import *
import keyboard

end_position_lose = 0
end_position_gespannt = 0
position_werkstück_wechsel = 0
dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = WinDLL(dll_path)

print ("Epos Command Library geladen")
print(epos.VCS_GetDeviceNameSelection)
print ("VSC_OpenDevice gefunden: ", hasattr(epos, "VCS_OpenDevice"))

epos.VCS_GetErrorInfo.argtypes = [
    c_uint,
    c_char_p,
    c_uint
]

epos.VCS_OpenDevice.argtypes = [
    c_char_p, 
    c_char_p, 
    c_char_p, 
    c_char_p, 
    POINTER(c_uint)
    ]

epos.VCS_OpenDevice.restype = c_ulonglong

error_code = c_uint(0)


handle = epos.VCS_OpenDevice(
    b"EPOS4", 
    b"MAXON Serial V2", 
    b"USB", 
    b"USB0", 
    byref(error_code)
    )

node_id = 1
def aktuelle_position_auslesen(handle, node_id):
    #Funktionsdefinition
    epos.VCS_GetPositionIs.argtypes = [
        c_void_p,
        c_ushort,
        POINTER(c_int),
        POINTER(c_uint)
    ]

    epos.VCS_GetPositionIs.restype = c_int

    current_position = c_int()

    result = epos.VCS_GetPositionIs(
        handle,
        node_id,
        byref(current_position),
        byref(error_code)
    )

    if result:
        position = current_position.value
        print(f"Aktuelle Position: {position}")
        return position
    else:
        print(f"Fehler: {error_code.value}")
    

def gehe_zu_position(handle, node_id, position):
    epos.VCS_MoveToPosition(
        handle, node_id, position, 1, 1, byref(error_code)
    )
    
def position_einlesen(dokument):
    with open (dokument, "r") as f:
        position = int(f.read())
        print("Position:", position)
        return position
    
def position_speichern(dokument, position):
    with open(dokument, "w") as f:
            f.write(str(position))
            print("Position", position, "wurde in ", dokument, "gespeichert")
            


if 
    end_position_lose = aktuelle_position_auslesen(handle, node_id)
    position_speichern("end_position_lose.txt", end_position_lose)