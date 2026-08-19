from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = windll.LoadLibrary(dll_path)

print ("Epos Command Library geladen")
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

epos.VCS_OpenDevice.restype = c_void_p

error_code = c_uint(0)

buffer = create_string_buffer(256)

epos.VCS_GetErrorInfo(error_code.value, buffer, 256)

handle = epos.VCS_OpenDevice(
    b"EPOS4", 
    b"MAXON SERIAL V2", 
    b"USB", 
    b"USB0", 
    byref(error_code)
    )

print ("Handle: ", handle)
print ("Error code: ", error_code.value)
print ( "Fehlercode: ", buffer.value.decode("latin1"))
print (buffer.value.decode(errors="ignore"))
print ("Handle type: ", type(handle))