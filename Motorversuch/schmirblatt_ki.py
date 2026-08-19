from ctypes import *

dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll"

epos = windll.LoadLibrary(dll_path)

epos.VCS_OpenDeviceDlg.argtypes = [
    POINTER(c_uint)
]
error_code = c_uint()
name = create_string_buffer(256)
version= create_string_buffer(256)

epos.VCS_GetDriverInfo(
    name,
    256,
    version,
    256,
    byref(error_code)
)
epos.VCS_OpenDeviceDlg.restype = c_ulonglong

epos.VCS_OpenDeviceDlg.argtypes = [
    POINTER(c_uint)
]

epos.VCS_OpenDeviceDlg.restype = c_void_p

handle = epos.VCS_OpenDeviceDlg(
    byref(error_code)
)

print("Handle:", handle)
print("Handletype: ", type(handle))
print("Error:", error_code.value)
print("Name: ", name.value.decode(errors="ignore"))
print("Version: ", version.value.decode(errors="ignore"))