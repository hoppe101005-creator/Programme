import snap7
from controler import controler

plc = snap7.client.Client()

plc.connect(
    "192.168.6.4",
    0,
    1
)

print("Verbunden:", plc.get_connected())

if plc.get_connected():
    daten = plc.db_read(31, 3, 1)
    print(daten)

plc.disconnect()

controler2 = controler()
controler2.open_device()
print(hasattr(controler2, "VCS_GetCurrentIsAveragedEx"))

