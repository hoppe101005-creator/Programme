from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = windll.LoadLibrary(dll_path)

name = create_string_buffer(256)
end = c_int()

index = 1
error_code = c_uint()

epos.VCS_GetProtocolStackNameSelection.argtypes = [
c_ushort,
c_char_p,
c_uint,
POINTER(c_int),
POINTER(c_uint)
]

while True:
    result = epos.VCS_GetProtocolStackNameSelection(
        index,
        name,
        256,
        byref(end),
        byref(error_code)
    )
    if result == 0:
        break
    
    print(index, name.value.decode())
    index += 1