import snap7

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
