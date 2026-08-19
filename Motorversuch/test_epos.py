from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = WinDLL(dll_path)

epos.VCS_OpenDevice.restype = c_void_p

error = c_uint()

handle = epos.VCS_OpenDevice(
    b"EPOS4",
    b"MAXON SERIAL V2",
    b"USB",
    b"USB0",
    byref(error)
)

print("Handle:", handle)
print("Error:", error.value)