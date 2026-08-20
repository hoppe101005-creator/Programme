from ctypes import *
from controler import controler

handle = controler.open_device()

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